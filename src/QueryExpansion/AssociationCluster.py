import re
import collections
import heapq

import numpy as np
from nltk.corpus import stopwords

# returns a list of tokens
def tokenize_doc(doc_text, stop_words):
    tokens = []
    text = doc_text
    text = re.sub(r'[\n]', ' ', text)
    text = re.sub(r'[,-]', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub('[0-9]', '', text)
    text = text.lower()
    tkns = text.split(' ')
    tokens = [token for token in tkns if token not in stop_words and token != '' and not token.isnumeric()]
    return tokens

def build_association(id_token_map, vocab, query):
    association_list = []
    for i, voc in enumerate(vocab):
        for word in query.split(' '):
            c1, c2, c3 = 0, 0, 0
            for doc_id, tokens_this_doc in id_token_map.items():
                count0 = tokens_this_doc.count(voc)
                count1 = tokens_this_doc.count(word)
                c1 += count0*count1
                c2 += count0*count0
                c3 += count1*count1
            c1 /= (c1 + c2 + c3)
            if c1 != 0:
                association_list.append((voc, word, c1))
                
    return association_list

def make_association_clusters(query, results, top_n=3):
    query_size = len(query.split(' '))
    stop_words = set(stopwords.words('english'))
    tokens = []
    tokens_map = {}

    for result in results:
        tokens_this_document = tokenize_doc(result['content'], stop_words)
        tokens_map[result['digest']] = tokens_this_document
        tokens.append(tokens_this_document)
        
    vocab = set([token for tokens_this_doc in tokens for token in tokens_this_doc])   
    association_list = build_association(tokens_map, vocab, query)
    association_list.sort(key = lambda x: x[2],reverse=True)

    # ignoring the first <query_size> number of terms, as they will be the same as terms in the query
    # using the next top_n terms
    extra_terms_list = [element[0] for element in association_list[query_size : query_size+top_n]]
    extra_terms = ' '.join(extra_terms_list)

    return query + ' ' + extra_terms
