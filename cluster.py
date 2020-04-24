import pickle, os
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity 

def main():

	load = True

	print('Document vectors are loaded!')
	doc_vectors = unpickle_item('docvec')
	print(doc_vectors.shape)

	vectorizer = unpickle_item('vectorizer')
	print('vectorizer is loaded')

	doc2vec = map_doc_to_vector(doc_vectors) # for getting the corresponding tfidf vector for each documents

	# print(doc2vec)
	search_query = ['olympic winner london']

	## TODO : apply text processing on search query

	transformed_query = vectorizer.transform(search_query)
	
	
	if load is True:
		kmeans = unpickle_item('cluster')
	else:
		kmeans = KMeans(n_clusters=10, random_state=0).fit(doc_vectors)
		pickle_item(kmeans, 'cluster')

		## TODO : apply agglomerative clustering

	
	labels = np.array(kmeans.labels_)
	
	doc_list = np.array(os.listdir('Webpages'))

	webpage_cluster = {}

	# assign clusters to documents 
	for label in np.unique(labels):
		webpage_cluster[label] = doc_list[ np.where(labels == label) ]

	## CLUSTERING DONE


	## QUERY EXPANSION ##

	# all the documents from the predicted cluster
	predicted_docs = webpage_cluster[ kmeans.predict(transformed_query)[0]]

	# get the additional terms 
	new_terms = expand_query(transformed_query, predicted_docs, doc2vec, vectorizer)

	print(new_terms)


def expand_query(query, docs, doc2vec, vectorizer):

	scores = np.array([cosine_similarity(query, doc2vec[doc])[0][0] for doc in docs])
	
	# get the top 10 document indices by cosine score
	top_indices = np.argsort(scores)[-10:]

	doc_list = os.listdir('Webpages/')

	# dictionary for mapping terms to their weights
	max_term_weights = {}
	
	for i in top_indices:

		doc_name = doc_list[i]	

		vector = doc2vec[ doc_name ] # tfidf vector for a document

		terms = vectorizer.inverse_transform(vector)[0]	# get the terms corresponding to those tfidf weights
		nonzero_vector = np.array(vector[ vector.nonzero() ])[0]	# convert the sparse matrix to an array with only the weights


		# assign the max weights of a term to that term in the dictionary
		for t,ti in zip(terms, range(len(terms))):

			if t in max_term_weights:
				if nonzero_vector[ti] > max_term_weights[t]:
					max_term_weights[t] = nonzero_vector[ti]
			else:
				max_term_weights[t] = nonzero_vector[ti]

	top_terms = Counter(max_term_weights).most_common(5) 	# get the top 5 terms with highets ewight

	return [term[0] for term in top_terms]





def map_doc_to_vector(doc_vectors):

	doc2vec = {}

	doc_list = os.listdir('Webpages')

	for i,dname in zip(range(len(doc_list)), doc_list):

		doc2vec[ dname ] = doc_vectors[i]

	return doc2vec 



def unpickle_item(filename):
	
	infile = open(filename, 'rb')
	unpickled_item = pickle.load(infile)
	infile.close()

	return unpickled_item


def pickle_item(item, filename):

	outfile = open(filename, 'wb')
	pickle.dump(item, outfile)
	outfile.close()


if __name__ == "__main__":
	main()

