#TF_IDF_calculator.py
import math
import json
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
# Download NLTK resources (needed for lemmatization)
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import pickle

#Helpers
def termFrequency(termOccurences, docLength):
    return termOccurences / docLength

def inverseDocumentFrequency(docTotal, termDoc):
    return math.log(docTotal / (termDoc + 1))

def tf_idf(tf, idf):
    return tf * idf

def findTF_IDF():
    #load databases
    with open('data.pickle', 'rb') as f:
        inverted_index = pickle.load(f)
    with open('doc_info.pickle', 'rb') as f:
        docId_docLength = pickle.load(f)
    num_documents = len(docId_docLength)
    
    for key, value in inverted_index.items():
        print(f"{key} TF-IDF Score")
        #create new data structure to track doc_ID: TF-IDF
        for doc_ID, index_List in value[0].items():
            #Calculate TF
            termOccurences = len(index_List) #Occurences of token in doc_ID
            docLength = docId_docLength[doc_ID] #Retrieve the length of the doc from helper dictionary
            tf = termFrequency(termOccurences, docLength)
            #Calculate IDF
            docTotal = num_documents
            
            docsContainingTerm = len(value[0].keys())
            
            
            if key == "msherk":
                print(f'total documents: {docTotal}')
                print(f'Docs that contain term: {docsContainingTerm}')
                
            idf = inverseDocumentFrequency(docTotal, docsContainingTerm)
            #Calculate TF-IDF
            score = tf_idf(tf,idf)
            #Record
            value[1][doc_ID] = score
        
    
    
    #Store updated Inverted Index
    with open('data.pickle', 'wb') as f:
        inverted_index = pickle.dump(inverted_index, f)

def getSizeKB():
    pickle_size_bytes = os.path.getsize('data.pickle')
    return pickle_size_bytes / 1024
     
if __name__ == '__main__':
    #Find TF-IDF scores
    findTF_IDF()
    
    with open('data.pickle', 'rb') as f:
        existing_data = pickle.load(f)
        
    with open('doc_info.pickle', 'rb') as f:
        docId_docLength = pickle.load(f)
        
    #NEW INDEX STATISTICS
    #number of documents
    print(f"TOTAL DOCUMENTS: {len(docId_docLength)}")
    
    #number of unique words
    uniqueWords =len(existing_data)
    print(f"UNIQUE WORDS: {uniqueWords}")
    
    #size in KB
    size = getSizeKB()
    print(f"INDEX SIZE: {(size):.0f} KB")
    
    #python TF_IDF_calculator.py