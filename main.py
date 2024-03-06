import math
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

def run(base):
    total_num_documents = getSubDirectories(base)
    return total_num_documents

def getSizeKB():
    pickle_size_bytes = os.path.getsize('data.pickle')
    return pickle_size_bytes / 1024

if __name__ == '__main__':
    webpages = sys.argv[1]
    total_num_docs = run(webpages)
    
    with open('data.pickle', 'rb') as f:
        existing_data = pickle.load(f)
    
    #INDEX STATISTICS
    #number of documents
    print(f"TOTAL DOCUMENTS: {total_num_docs}")
    
    #number of unique words
    uniqueWords =len(existing_data)
    print(f"UNIQUE WORDS: {uniqueWords}")
    
    #size in KB
    size = getSizeKB()
    print(f"INDEX SIZE: {(size):.0f} KB")
    
    
#python main.py "C:\Users\kylej\OneDrive\Documents\UCI\CS 121\Assignment 3\WEBPAGES_RAW"