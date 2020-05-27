import pickle

def unpickle_item(filename):
	
	filename = 'Serialized/' + filename
	infile = open(filename, 'rb')
	unpickled_item = pickle.load(infile)
	infile.close()

	return unpickled_item


def pickle_item(item, filename):

	filename = 'Serialized/' + filename
	outfile = open(filename, 'wb')
	pickle.dump(item, outfile)
	outfile.close()
