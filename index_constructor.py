'''
Builds the inverted index
1. Remove stop words from extracted tokens
2. Apply lemmatization on tokens
3. Store TF-IDF on every term/document
'''
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

#Open and read all files in the main/base directory
def getSubDirectories(baseDirectory):
    
    #obtain list of all valid subdirectories
    subdirectories = [
        os.path.join(baseDirectory, sub)
        for sub in os.listdir(baseDirectory)
        if os.path.isdir(os.path.join(baseDirectory, sub))
    ]
    
    inverted_index = {} # word1: [{doc_ID : indexList, ...},{doc_id : TF-IDF, ...}], word2: ...
    num_documents = 0
    docId_docLength = {}
    
    #Temporary test loop - i subdirectories - FOR TESTING ONLY
    
    for i in range(len(subdirectories)): #len(subdirectories)
        #read all files and get data
        directory_file_data = readAllFiles(subdirectories[i])
        documentIDs = directory_file_data[0]
        word_occurences = directory_file_data[1]
        tf_idf_scores = directory_file_data[2] #unused but don't delete or it might break everything
        subdirectory_num_documents = directory_file_data[3]
        documentID_Length_dict = directory_file_data[4]
        
        #update document length dictionary
        for key, value in documentID_Length_dict.items():
            docId_docLength[key] = value
            
        #update document count in index
        num_documents += subdirectory_num_documents
        for j in range(len(documentIDs)):
            print(f"UPLOADING DOCUMENT: {documentIDs[i]}")
            #Check if the word already exists in dict
            document_word_occurences = word_occurences[j]
            for word in document_word_occurences:
                print(f"Updating {word}")
                
                #add word to index and record document occurence
                if word not in inverted_index:
                    occurences = []
                    index_doc_dic = {}
                    inverted_index[word] = [occurences]
                    inverted_index[word][0] = index_doc_dic
                    inverted_index[word][0][documentIDs[j]] = []
                else:
                    inverted_index[word][0][documentIDs[j]] = []
                    #inverted_index[word][0].append({documentIDs[j] : []})
        
        #update word index occurences in inverted index
        track = 0
        for document in word_occurences: #interate over the words
            print(f"TRACKING DOCUMENT: {documentIDs[track]}")
            for word in document:
                whichDoc = documentIDs[track]
                #print(whichDoc)
                inverted_index[word][0][whichDoc].extend(document[word])
            track += 1
            
    #Add extra indicies for tf-idf storage 
    for key, value in inverted_index.items():
            TF_IDF_empty = {}
            value.append(TF_IDF_empty)
            
    #pickle the modified data            
    with open('data.pickle', 'wb') as f:
        pickle.dump(inverted_index, f)
        
    with open('doc_info.pickle', 'wb') as f:
        pickle.dump(docId_docLength, f)
        
    return num_documents      


def readAllFiles(subdirectory):
    #all incidies correspond to the same file
    files_documentID_list = []
    files_document_word_occurences = []
    files_tf_idf = []
    num_documents = 0
    documentID_Length_dict = {}
    
    #get list of stop words
    stop_words = set(stopwords.words('english'))
    total_files_read = 0
    for filename in os.listdir(subdirectory):
        '''
        #temporary stop for testing
        if total_files_read > 20:
            break
        '''
        file_contents = ""
        
        file_path = os.path.join(subdirectory, filename)
        if os.path.isfile(file_path):  # Check if it's a file
            # Read the file content
            try:  
                with open(file_path, 'r', encoding='utf-8') as file:
                    #read file
                    content = file.read()
                    file_contents = content
                    total_files_read += 1
            except: #bad file
                continue
        else: #not a file type
            continue

        #now that file contents have been successfully read...
        num_documents += 1
        #parse the file contents and extract words from the html source cope
        soup = BeautifulSoup(file_contents, 'html.parser')
        text_content = soup.get_text(separator=' ') #string
        
        #get documentID
        documentID = f"{os.path.basename(subdirectory)}/{os.path.basename(filename)}"
        
        #print(f"DocumentID: {documentID}")
        #tokenize file content
        tokens = tokenize(text_content)
        
        #record document length
        documentID_Length_dict[documentID] = len(tokens)
        
        #lemmatize non-stop word tokens (include stop words)
        lemmatized_with_stopwords = []
        stopword_or_not = []
        for token in tokens:
            if token.lower() not in stop_words and token.lower().isalnum() and not token.lower().isnumeric() and token.lower().isascii(): #add to lemmatized if not a stop word, is alphanumeric, is not a number, and is ascii
                stopword_or_not.append(False)
                lemmatized_with_stopwords.append(lemmatizeString(token.lower()))
            elif token.lower().isalnum(): #track index other valid tokens
                stopword_or_not.append(True)
                lemmatized_with_stopwords.append(token.lower())
            else:
                pass
            
        #record index occurences
        word_index_occurence = {} # word : []
        for i in range(0,len(stopword_or_not)):
            #if not a stop word (false)
            if not stopword_or_not[i]:
                #check if word has already been added to dict
                if lemmatized_with_stopwords[i] in word_index_occurence:
                    word_index_occurence[lemmatized_with_stopwords[i]].append(i)
                else:
                    word_index_occurence[lemmatized_with_stopwords[i]] = [i]     
                          
        files_documentID_list.append(documentID)
        files_document_word_occurences.append(word_index_occurence)
        
        print(f"READING DOCUMENT: {documentID}")
        
    return files_documentID_list, files_document_word_occurences, files_tf_idf, num_documents, documentID_Length_dict
        
def tokenize(text):
    tokens = word_tokenize(text)
    return tokens

def lemmatizeString(token):
    lemmatizer = WordNetLemmatizer()
    lemmatized_token = lemmatizer.lemmatize(token)
    return lemmatized_token

def lemmatizeList(validTokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) 
                         for token in validTokens]
    return lemmatized_tokens
            
'''
DATABASE structure

documentID = “folder_number/file_number” 

Folder: inverted_index
    word1.txt
        {documentID1 : [ [indicies of occurence], wordFrequency, Tf-idf score ], ... }
    word2.txt

    ...

    wordX.txt


'''