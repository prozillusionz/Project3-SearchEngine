#basic_query.py
import json
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import pickle

# Getting associated docuemtns related to a search query
def get_documents(query_term):
    words = query_term.split()
    with open('data.pickle', 'rb') as f:
        existing_data = pickle.load(f)
    # Check if the first word of the search query exists in the data and is a list
    if isinstance(existing_data[words[0]], list):
        documents = set()
        # Each dictionary in the list of the first word
        for doc_dict in existing_data[words[0]]:
            if isinstance(doc_dict, dict):
                #Add the keys (document IDs) to the set of documents
                documents |= set(doc_dict.keys())
    else:
        #print(f"existing_data[words[0]] is not a list of dictionaries")
        return [] # Empty List
    # Remaining words in the query term
    for word in words[1:]:
        # Check if the word of the search query exists in the data and is a list
        if word in existing_data and isinstance(existing_data[word], list):
            word_documents = set()
            # Each dictionary in the list of the current word
            for doc_dict in existing_data[word]:
                if isinstance(doc_dict, dict):
                    # Add the keys (document IDs) to the set of documents of the current word
                    word_documents |= set(doc_dict.keys())
            # Update the set of documents
            documents &= word_documents # Intersection of sets
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