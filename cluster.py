import pickle, os, sys
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity 
import pickler 
import textprocessor as tp

# RUN python cluster.py 0 / 1 kmeans / agg

def main():

	load = bool(int(sys.argv[1]))
	clustering_type = sys.argv[2]
	n_clusters = int(sys.argv[3])
	# print(load)

	
	doc_vectors = pickler.unpickle_item('docvec')
	print('Document vectors are loaded!')
	print(doc_vectors.shape)

	vectorizer = pickler.unpickle_item('vectorizer')
	print('vectorizer is loaded')

	doc_contents = np.array(pickler.unpickle_item('doc_contents'))
	url_list = np.array(pickler.unpickle_item('url_list'))
	
	
	if load is True:
		kmeans = pickler.unpickle_item('cluster')
	else:
		if clustering_type == 'kmeans':
			cluster = KMeans(n_clusters=n_clusters, random_state=0).fit(doc_vectors)
			pickler.pickle_item(cluster, 'cluster')
		elif clustering_type == 'agg':
			cluster = AgglomerativeClustering(n_clusters=n_clusters, random_state=0).fit(doc_vectors)
			pickler.pickle_item(cluster, 'cluster')

	
	labels = np.array(cluster.labels_)
	
	# doc_list = np.array(os.listdir('Webpages'))

	webpage_cluster = {}

	# assign clusters to documents 
	for label in np.unique(labels):
		doc_indices = np.where(labels == label)
		webpage_cluster[label] = (url_list[ doc_indices] , doc_contents[ doc_indices ] )

	pickler.pickle_item(webpage_cluster, 'webpage_cluster')
	print('Clustering complete and serialized')


if __name__ == "__main__":
	main()

