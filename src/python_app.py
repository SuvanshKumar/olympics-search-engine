import flask
from flask_cors import CORS
import pysolr
import re
from flask import request, jsonify
import pickler
from QueryExpansion import MetricClusters
from QueryExpansion import AssociationCluster
from QueryExpansion import ScalarClusters
import json

# Create a client instance. The timeout and authentication options are not required.
solr_vector = pysolr.Solr('http://localhost:8983/solr/project_index_vector/', always_commit=True, timeout=10)
solr_page_rank = pysolr.Solr('http://localhost:8983/solr/project_index_pagerank/', always_commit=True, timeout=10)
pickle_file1 = r"webpage_cluster_inverse"
k_means_cluster_mapping = pickler.unpickle_item(pickle_file1)
pickle_file2 = r'webpage_agg_cluster_inverse'
agg_cluster_mapping = pickler.unpickle_item(pickle_file2)
with open('authority_score.json','r') as authority_score_file:
    authority_score_dict = json.load(authority_score_file)
# authority_score_dict = authority_score_dict.replace("'",",")
# authority_score_dict = json.loads(authority_score_dict.replace(',','"'))

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/api/v1/indexer', methods=['GET'])
def get_query():
    if 'query' in request.args and 'type' in request.args:
        query = str(request.args['query'])
        type =  str(request.args['type'])

        if "clustering" in type:
            if 'kmeans' in type:
                solr_results = get_results_from_solr_page_rank(query)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    response = make_response(solr_results)
                    response = get_kmeans_clustering_results(response)
                    result = {"query":query,"response":response}
            elif 'agglomerative' in type:
                solr_results = get_results_from_solr_page_rank(query)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    response = make_response(solr_results)
                    response = get_agglomerative_clustering_results(response)
                    result = {"query":query,"response":response}
        elif type == "page_rank":
            solr_results = get_results_from_solr_page_rank(query)
            if solr_results.hits == 0:
                return jsonify("query out of scope")
            else:
                response = make_response(solr_results)
                result = {"query":query,"response":response}
        elif type == "vector":
            solr_results = get_results_from_solr_vector(query)
            if solr_results.hits == 0:
                return jsonify("query out of scope")
            else:
                response = make_response(solr_results)
                result = {"query":query,"response":response}
        elif "query_expansion" in type:
            expansion_terms = 3
            if 'association' in type:
                solr_results = get_results_from_solr_page_rank(query)
                expanded_query = AssociationCluster.make_association_clusters(query, solr_results, top_n = expansion_terms)
                solr_results = get_results_from_solr_page_rank(expanded_query)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    response = make_response(solr_results)
                    result = {"query":expanded_query,"response":response}
                pass
            elif 'metric' in type:
                solr_results = get_results_from_solr_page_rank(query)
                expanded_query = MetricClusters.make_metric_clusters(query, solr_results, top_n = expansion_terms)
                solr_results = get_results_from_solr_page_rank(expanded_query)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    response = make_response(solr_results)
                    result = {"query":expanded_query,"response":response}
                pass
            elif 'scalar' in type:
                solr_results = get_results_from_solr_page_rank(query)
                expanded_query_scalar = ScalarClusters.make_scalar_clusters(query, solr_results)
                solr_results = get_results_from_solr_page_rank(expanded_query_scalar)
                if solr_results.hits == 0:
                    return jsonify("query out of scope")
                else:
                    response = make_response(solr_results)
                    result = {"query":expanded_query_scalar,"response":response}
            # elif 'rocchio' in type:
            #     pass
        elif type == "hits":
            solr_results = get_results_from_solr_page_rank(query)
            if solr_results.hits == 0:
                return jsonify("query out of scope")
            else:
                response = make_response(solr_results)
                response = get_result_from_hits(response)
                result = {"query":query,"response":response}
            # Write code to integrate query expansion

        return jsonify(result)
    else:
        return "Error: No query or type provided"

def make_response(solr_results):
    api_resp = list()
    rank = 0
    for result in solr_results:
        rank += 1
        if 'title' in result:
            title = result["title"]
        else:
            title = " "
        url = result["url"]
        content = result["content"]
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

def get_kmeans_clustering_results(clust_inp):
    for result in clust_inp:
        curr_url = result['url']
        curr_cluster = k_means_cluster_mapping.get(curr_url,'99')
        result.update({"cluster":curr_cluster})
        result.update({"done":"False"})
    clust_resp = []
    curr_rank = 1
    for curr_resp in clust_inp:
        if curr_resp["done"] == "False":
            curr_cluster = curr_resp["cluster"]
            curr_resp.update({"done": "True"})
            curr_resp.update({"rank": str(curr_rank)})
            curr_rank += 1
            clust_resp.append({"title": curr_resp["title"], "url": curr_resp["url"],
                               "meta_info": curr_resp["meta_info"], "rank": curr_resp["rank"]})
            for remaining_resp in clust_inp:
                if remaining_resp["done"] == "False":
                    if remaining_resp["cluster"] == curr_cluster:
                        remaining_resp.update({"done": "True"})
                        remaining_resp.update({"rank": str(curr_rank)})
                        curr_rank += 1
                        clust_resp.append({"title": remaining_resp["title"], "url": remaining_resp["url"],
                                           "meta_info": remaining_resp["meta_info"], "rank": remaining_resp["rank"]})

    return clust_resp

def get_agglomerative_clustering_results(clust_inp):
    for result in clust_inp:
        curr_url = result['url']
        curr_cluster = agg_cluster_mapping.get(curr_url,'99')
        result.update({"cluster":curr_cluster})
        result.update({"done":"False"})
    clust_resp = []
    curr_rank = 1
    for curr_resp in clust_inp:
        if curr_resp["done"] == "False":
            curr_cluster = curr_resp["cluster"]
            curr_resp.update({"done": "True"})
            curr_resp.update({"rank": str(curr_rank)})
            curr_rank += 1
            clust_resp.append({"title": curr_resp["title"], "url": curr_resp["url"],
                               "meta_info": curr_resp["meta_info"], "rank": curr_resp["rank"]})
            for remaining_resp in clust_inp:
                if remaining_resp["done"] == "False":
                    if remaining_resp["cluster"] == curr_cluster:
                        remaining_resp.update({"done": "True"})
                        remaining_resp.update({"rank": str(curr_rank)})
                        curr_rank += 1
                        clust_resp.append({"title": remaining_resp["title"], "url": remaining_resp["url"],
                                           "meta_info": remaining_resp["meta_info"], "rank": remaining_resp["rank"]})

    return clust_resp

def get_result_from_hits(result_set):
    result_set = sorted(result_set,key=lambda x:authority_score_dict.get(x['url'],0.0),reverse=True)
    return result_set

app.run(port='5000')