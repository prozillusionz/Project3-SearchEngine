#query_main.py
import json
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import pickle
from index_constructor import *
from basic_query import *

def query_word(queryWord):
    word_urls = returnURLS(get_documents(queryWord))
    return word_urls

def getInfo(query):
    word_urls = query_word(query.lower())
    number_urls = len(word_urls)
    return number_urls, word_urls

    
if __name__ == '__main__':
    queryWords = sys.argv[1:]
    for word in queryWords:
        results = getInfo(word.lower())
        num_urls = results[0]
        list_of_urls = results[1]
        print(f"Query: {word} | URLS: {num_urls}\n{list_of_urls[:20]}")