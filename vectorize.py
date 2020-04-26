import os, string, pickle, re, sys, time
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk.stem.porter import *
from nltk.corpus import stopwords
import textprocessor as tp
import pickler
import json

def main():

    path = 'index.json'

    with open(path, encoding="utf8") as json_file:
        res = json.load(json_file)

    docs = res['response']['docs']

    url_list = []
    doc_contents = []

    for doc in docs:
        if 'url' and 'content' in doc:
            url_list.append(doc['url'])
            doc_contents.append(doc['content'])

    pickler.pickle_item(url_list, 'url_list')
    pickler.pickle_item(doc_contents, 'doc_contents')

    print('Text Processing . . .') 
    tokens = tp.tokenize_docs(doc_contents)
   
    filtered_tokens = tp.remove_stopwords(tokens)
    print('Done.')

    print(len(filtered_tokens))
    # stems = tp.tem_tokens(filtered_tokens)

    print('Apply vectorizer . . ')
    apply_vectorization(filtered_tokens)
    print('Done.')


def apply_vectorization(tokens):

    processed_docs = []

    for doc in tokens:
    	processed_docs.append(' '.join(doc))

    vectorizer = TfidfVectorizer(use_idf=True).fit(processed_docs)
    
    doc_vectors = vectorizer.transform(processed_docs)


    pickler.pickle_item(doc_vectors, 'docvec')
    pickler.pickle_item(vectorizer, 'vectorizer')


if __name__ == "__main__":
    main()




