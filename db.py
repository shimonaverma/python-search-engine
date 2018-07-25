# from operator import itemgetter
from __future__ import print_function
from math import log, sqrt
from collections import defaultdict
import nltk, io
import sys
import numpy as np
import pickle

inverted_index = defaultdict(list)
nos_of_documents = 0
vects_for_docs = []  # we will need nos of docs number of vectors, each vector is a dictionary
document_freq_vect = {}  # sort of equivalent to initializing the number of unique words to 0
word_line_array = []

def main(arg):
    global nos_of_documents
    nos_of_documents = int(arg)+1
    
if __name__ == "__main__":
    x= main(sys.argv[1])


# this is the first function that is executed.
# It updates the vects_for_docs variable with vectors of all the documents.
def iterate_over_all_docs():
    for i in range(nos_of_documents - 1):
        doc_text = get_document_text_from_doc_id(i)
        token_list = get_tokenized_and_normalized_list(doc_text)
        vect = create_vector(token_list)
        vects_for_docs.append(vect)

        vect1 = get_word_line(doc_text)
        word_line_array.append(vect1)


# name is self explanatory, it generates and inverted index in the global variable inverted_index,
# however, precondition is that vects_for_docs should be completely initialized
def generate_inverted_index():
    count1 = 0
    for vector in vects_for_docs:
        for word1 in vector:
            inverted_index[word1].append(count1)
        count1 += 1


# it updates the vects_for_docs global variable (the list of frequency vectors for all the documents)
# and changes all the frequency vectors to tf-idf unit vectors (tf-idf score instead of frequency of the words)
def create_tf_idf_vector():
    vect_length = 0.0
    for vect in vects_for_docs:
        for word1 in vect:
            word_freq = vect[word1]
            temp = calc_tf_idf(word1, word_freq)
            vect[word1] = temp
            vect_length += temp ** 2

        vect_length = sqrt(vect_length)
        for word1 in vect:
            vect[word1] /= vect_length



# precondition: word is in the document_freq_vect
# this function calculates the tf-idf score for a given word in a document
def calc_tf_idf(word1, word_freq):
    return log(1 + word_freq) * log(nos_of_documents / document_freq_vect[word1])


# define a number of functions,
# function to to read a given document word by word and
# 1. Start building the dictionary of the word frequency of the document,
#       2. Update the number of distinct words
#  function to :
#       1. create the dictionary of the term freqency (number of documents which have the terms);




# this function returns a list of tokenized and stemmed words of any text
def get_tokenized_and_normalized_list(doc_text):
    # return doc_text.split()


    tokens = nltk.word_tokenize(doc_text)
    ps = nltk.stem.PorterStemmer()
    stemmed = []
    for words in tokens:
        stemmed.append(ps.stem(words))
    return stemmed


# creates a vector from a list (l1) , vector is a dictionary, containing words:frequency pairs
# this function should not be called to parse the query given by the user
# because this function also updates the document frequency dictionary
def create_vector(l1):
    vect = {}  # this is a dictionary
    global document_freq_vect

    for token in l1:
        if token in vect:
            vect[token] += 1
        else:
            vect[token] = 1
            if token in document_freq_vect:
                document_freq_vect[token] += 1
            else:
                document_freq_vect[token] = 1
    return vect


def get_word_line(doc_text):
    tokens = nltk.tokenize.line_tokenize(doc_text)
    ps = nltk.stem.PorterStemmer()
    j=1
    vect = {}

    for line in tokens:
        ansh=nltk.tokenize.word_tokenize(line)
        for words in ansh :
            words = ps.stem(words)
            if words in vect.keys():
                vect[words] = vect[words] + str(j).zfill(3) 
            else:
                vect[words] = str(j).zfill(3)

        j = j+1;

    return vect

def get_document_text_from_doc_id(doc_id):
    # noinspection PyBroadException
    try:
        str1 = io.open("corpus/doc" + str(doc_id).zfill(4)).read()
    except:
        str1 = ""
    return str1


# now the actual execution starts (this is equivalent to the main function of java)


# initializing the vects_for_docs variable
iterate_over_all_docs()

# self explanatory
generate_inverted_index()

# changes the frequency values in vects_for_docs to tf-idf values
create_tf_idf_vector()

for i in range(nos_of_documents-1):
    if i==0:
        with open("/home/godfather/Documents/text-search-engine-master/db1.txt",'w') as file:
            file.write(pickle.dumps(vects_for_docs[i]))
        with open("/home/godfather/Documents/text-search-engine-master/db2.txt",'w') as file1:
            file1.write(pickle.dumps(word_line_array[i]))
    else:
        with open("/home/godfather/Documents/text-search-engine-master/db1.txt",'a') as file:
            file.write(pickle.dumps(vects_for_docs[i]))
        with open("/home/godfather/Documents/text-search-engine-master/db2.txt",'a') as file1:
            file1.write(pickle.dumps(word_line_array[i]))

