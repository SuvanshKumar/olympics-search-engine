import os, string, pickle, re, sys, time
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk.stem.porter import *
from nltk.corpus import stopwords



def main():

    path = 'Crawler/Webpages/'
    tokens = tokenize_docs(path)
   
    filtered_tokens = remove_stopwords(tokens)

    # stems = stem_tokens(filtered_tokens)
    apply_vectorization(filtered_tokens)


def apply_vectorization(tokens):

    processed_docs = []

    for doc in tokens:
    	processed_docs.append(' '.join(doc))

    vectorizer = TfidfVectorizer(use_idf=True).fit(processed_docs)
    
    doc_vectors = vectorizer.transform(processed_docs)

    print(doc_vectors)

    pickle_item(doc_vectors, 'docvec')
    pickle_item(vectorizer, 'vectorizer')
    


def remove_stopwords(tokens):

	stop_words = set(stopwords.words('english'))

	filtered_tokens = []

	for token in tokens:
		filtered_tokens.append([t for t in token if t not in stop_words and len(t) > 1])

	return filtered_tokens


def stem_tokens(tokens):

    stemmer = PorterStemmer()
    
    stems = []

    for token in tokens:
    	stems.append([stemmer.stem(t) for t in token])


    return stems


def tokenize_docs(path):
	"""Iterates through the list of documents, processes and tokenizes text
	
	Args:
	    path (string): path to the documents """
	doc_list = os.listdir(path)
	tokens = []

	# print(doc_list[len(doc_list)-1])
	for i,doc in zip(range(len(doc_list)), doc_list):
	    f = open(path + doc, 'r')
	    text = f.read()

	    text = process_raw_text(text)

	    doc_tokens = text.split()


	    tokens.append(doc_tokens)

	return tokens



def process_raw_text(text):
    """Applies different processing techniques on text
    
    Args:
        text (string): a document as text
    
    Returns:
        string: processed document
    """
    punctuation_dict = dict.fromkeys(string.punctuation,' ')

    text = text.lower()		# convert to lowercase
    text = text.replace('\\n', ' ')
    text = re.sub('[0-9]', '',text)		# TODO remove digits but keep years
    text = re.sub(r'(?<!\w)([a-z])\.', r'\1', text)		# remove periods from acronmys, e.g: U.S.A -> USA
    
    text = expand_contractions(text)
    
    text = text.translate(str.maketrans(punctuation_dict)).strip() # remove punctuations
    return text



def expand_contractions(text):
    """expands common contractions in english language
    
    Args:
        text (string): a document as text
    
    Returns:
        string: document with all contractions expanded
    """
    common_contractions = [("'m", " am"), ("n't", " not"), ("'ve", " have"), ("'ll", " will"), ("'s", "s"), ("'d", " would")]
    for cc in common_contractions:
        text = re.sub(cc[0], cc[1], text)
    return text


def pickle_item(item, filename):

	outfile = open(filename, 'wb')
	pickle.dump(item, outfile)
	outfile.close()




if __name__ == "__main__":
    main()




