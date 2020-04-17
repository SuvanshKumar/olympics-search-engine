import pickle, os
import numpy as np
from sklearn.cluster import KMeans


def main():

	load = True

	print('Document vectors are loaded!')
	doc_vectors = unpickle_item('docvec')
	print(doc_vectors.shape)

	vectorizer = unpickle_item('vectorizer')
	print('vectorizer is loaded')
	print(vectorizer)

	search_query = ['olympic winner swimming']

	tq = vectorizer.transform(search_query)
	
	if load is True:
		kmeans = unpickle_item('cluster')
	else:
		kmeans = KMeans(n_clusters=10, random_state=0).fit(doc_vectors)
		pickle_item(kmeans, 'cluster')

	
	labels = np.array(kmeans.labels_)
	
	doc_list = np.array(os.listdir('Webpages'))

	webpage_cluster = {}

	for label in np.unique(labels):
		webpage_cluster[label] = doc_list[ np.where(labels == label) ]


	print(webpage_cluster[kmeans.predict(tq)[0]])


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

