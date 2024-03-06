#basic_query.py
import json
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import pickle

def get_documents(query_term):
    words = query_term.split()
    with open('data.pickle', 'rb') as f:
        existing_data = pickle.load(f)
    if isinstance(existing_data[words[0]], list):
        documents = set()
        for doc_dict in existing_data[words[0]]:
            if isinstance(doc_dict, dict):
                documents |= set(doc_dict.keys())
    else:
        #print(f"existing_data[words[0]] is not a list of dictionaries")
        return []
    for word in words[1:]:
        if word in existing_data and isinstance(existing_data[word], list):
            word_documents = set()
            for doc_dict in existing_data[word]:
                if isinstance(doc_dict, dict):
                    word_documents |= set(doc_dict.keys())
            documents &= word_documents  # intersection of sets
        else:
            #print(f"Word '{word}' not found in existing data.")
            return []  # return an empty list if the word is not found to prevent keyerror
    return list(documents)
  
def returnURLS(document_ids):
    urls = []
    bookeeper = r'C:\Users\kylej\OneDrive\Documents\UCI\CS 121\Assignment 3\WEBPAGES_RAW\bookkeeping.json'
    with open(bookeeper, 'r') as f:
        data = json.load(f)
        
    for document in document_ids:
        document_key = str(document)
        if document_key in data:
            url = data[document_key]
            urls.append(url)
            #print(f"Document ID: {document_key}, URL: {url}")
    
    return urls