import flask
from flask_cors import CORS
import pysolr
import re
from flask import request, jsonify
import pickler
from QueryExpansion import MetricClusters

# Create a client instance. The timeout and authentication options are not required.
solr_vector = pysolr.Solr('http://localhost:8983/solr/project_index_vector/', always_commit=True, timeout=10)
solr_page_rank = pysolr.Solr('http://localhost:8983/solr/project_index_pagerank/', always_commit=True, timeout=10)

app = flask.Flask(_name_)
CORS(app)
app.config["DEBUG"] = True


@app.route('/api/v1/indexer', methods=['GET'])
def get_query():
    if 'query' in request.args and 'type' in request.args:
        query = str(request.args['query'])
        type =  str(request.args['type'])

        if "clustering" in type:
            search_result = get_clustering_results(query, type)
            result = {"query":query,"response":search_result}
        elif type == "page_rank":
            solr_results = get_results_from_solr_page_rank(query)
            if solr_results.hits == 0:
                return jsonify("query out of scope")
            else:
                result = make_response(solr_results)
        elif type == "vector":
            solr_results = get_results_from_solr_vector(query)
            if solr_results.hits == 0:
                return jsonify("query out of scope")
            else:
                result = make_response(solr_results)
        elif "query_expansion" in type:
            expansion_terms = 3
            if 'association' in type:
                solr_results = get_results_from_solr_page_rank(query)
                expanded_query = AssociationCluster.make_association_clusters(query, results, top_n = expansion_terms)
                solr_results = get_results_from_solr_page_rank(expanded_query)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    result = make_response(solr_results)
                pass
            elif 'metric' in type:
                solr_results = get_results_from_solr_page_rank(query)
                expanded_query = MetricClusters.make_metric_clusters(query, solr_results, top_n = expansion_terms)
                solr_results = get_results_from_solr_page_rank(expanded_query)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    result = make_response(solr_results)
                pass
            elif 'scalar' in type:
                pass
            elif 'rocchio' in type:
                pass

            # Write code to integrate query expansion

        return jsonify(result)
    else:
        return "Error: No query or type provided"

def make_response(solr_results):
    api_resp = list()
    rank = 0
    for result in solr_results:
        rank += 1
        title = result['title']
        url = result['url']
        content = result['content']
        meta_info = content[:200]
        meta_info = meta_info.replace("\n", " ")
        meta_info = " ".join(re.findall("[a-zA-Z]+", meta_info))
        link_json = {"title": title,"url": url,"meta_info": meta_info,"rank": rank}
        api_resp.append(link_json)
    return api_resp


def get_results_from_solr_page_rank(query):
    results = solr_page_rank.search(query, search_handler="/select", **{
        "wt": "json",
        "rows": 50
    })
    return results

def get_results_from_solr_vector(query):
    results = solr_vector.search(query, search_handler="/select", **{
        "wt": "json",
        "rows": 50
    })
    return results

app.run(port='5000')