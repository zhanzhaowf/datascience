# -*- coding: utf-8 -*-

import time
import re
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from collections import Counter
from functools import reduce
from multiprocessing import Pool, cpu_count


news = fetch_20newsgroups(subset='all')
print(len(news.data))
print(news.data[0])

data = news.data * 10
print(len(data))

    
def clean_word(word):
    return re.sub(r'[^\w\s]','',word).lower()

def word_not_in_stopwords(word):
    return word not in ENGLISH_STOP_WORDS and word and word.isalpha()

def mapper(text):
    tokens_in_text = text.split()
    tokens_in_text = map(clean_word, tokens_in_text)
    tokens_in_text = filter(word_not_in_stopwords, tokens_in_text)
    return Counter(tokens_in_text)

def reducer(cnt1, cnt2):
    cnt1.update(cnt2)
    return cnt1

def chunk_mapper(chunk):
    mapped = map(mapper, chunk)
    reduced = reduce(reducer, mapped)
    return reduced


def chunkify(lst, n_chunks):
    """Yield successive n-sized chunks from lst."""
    n = int(len(lst) / n_chunks)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]



n_cores = cpu_count()
print(n_cores)
pool = Pool(processes=n_cores - 1)
t2 = time.time()
data_chunks = chunkify(data, n_chunks=n_cores - 1)
#step 1:
mapped = pool.map(chunk_mapper, data_chunks)
#step 2:
reduced = reduce(reducer, mapped)
print(reduced.most_common(10))
print(time.time() - t2)
