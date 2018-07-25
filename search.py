# from operator import itemgetter
from __future__ import print_function
from math import log, sqrt
from collections import defaultdict
import nltk, io
import sys
import pickle

nos_of_documents = 0
vects_for_docs = []  # we will need nos of docs number of vectors, each vector is a dictionary
document_freq_vect = {}  # sort of equivalent to initializing the number of unique words to 0
word_line_array = []



with (open("/home/godfather/Documents/text-search-engine-master/db1.txt", "r")) as openfile:
    while True:
        try:
            vects_for_docs.append(pickle.load(openfile))
            
        except EOFError:
            break


with (open("/home/godfather/Documents/text-search-engine-master/db2.txt", "r")) as openfile1:
    while True:
        try:
            word_line_array.append(pickle.load(openfile1))
            
        except EOFError:
            break







def main(arg):
    global nos_of_documents
    nos_of_documents = int(arg)+1
    
if __name__ == "__main__":
    x= main(sys.argv[1])


# creates a vector from a query in the form of a list (l1) , vector is a dictionary, containing words:frequency pairs
def create_vector_from_query(l1):
    vect = {}
    for token in l1:
        if token in vect:
            vect[token] += 1.0
        else:
            vect[token] = 1.0
    return vect


# note: even though you do not need to convert the query vector into a unit vector,
# I have done so because that would make all the dot products <= 1
# as the name suggests, this function converts a given query vector
# into a tf-idf unit vector(word:tf-idf vector given a word:frequency vector
def get_tf_idf_from_query_vect(query_vector1):
    vect_length = 0.0
    for word1 in query_vector1:
        word_freq = query_vector1[word1]
        if word1 in document_freq_vect:  # I have left out any term which has not occurred in any document because
            query_vector1[word1] = calc_tf_idf(word1, word_freq)
        else:
            query_vector1[word1] = log(1 + word_freq) * log(nos_of_documents)  
            # this additional line will ensure that if the 2 queries,
            # the first having all words in some documents,
            #  and the second having and extra word that is not in any document,
            # will not end up having the same dot product value for all documents
        vect_length += query_vector1[word1] ** 2
    vect_length = sqrt(vect_length)
    if vect_length != 0:
        for word1 in query_vector1:
            query_vector1[word1] /= vect_length


# precondition: word is in the document_freq_vect
# this function calculates the tf-idf score for a given word in a document
def calc_tf_idf(word1, word_freq):
    return log(1 + word_freq) * log(nos_of_documents / document_freq_vect[word1])




# this function returns a list of tokenized and stemmed words of any text
def get_tokenized_and_normalized_list(doc_text):
    # return doc_text.split()


    tokens = nltk.word_tokenize(doc_text)
    ps = nltk.stem.PorterStemmer()
    stemmed = []
    for words in tokens:
        stemmed.append(ps.stem(words))
    return stemmed


# this function returns the dot product of vector1 and vector2
def get_dot_product(vector1, vector2):
    if len(vector1) > len(vector2):  # this will ensure that len(dict1) < len(dict2)
        temp = vector1
        vector1 = vector2
        vector2 = temp
    keys1 = vector1.keys()
    keys2 = vector2.keys()
    sum = 0
    for i in keys1:
        if i in keys2:
            sum += vector1[i] * vector2[i]
    return sum

def get_line_info(vector1, vector2):
    if len(vector1) > len(vector2):  # this will ensure that len(dict1) < len(dict2)
        temp = vector1
        vector1 = vector2
        vector2 = temp
    keys1 = vector1.keys()
    keys2 = vector2.keys()
    sum = "000"
    for i in keys1:
        if i in keys2:
            sum = sum + str(vector2[i]).zfill(3)
    return sum    

# this function takes the dot product of the query with all the documents
#  and returns a sorted list of tuples of docId, cosine score pairs
def get_result_from_query_vect(query_vector1):
    parsed_list = []
    for i in range(nos_of_documents - 1):
        dot_prod = get_dot_product(query_vector1, vects_for_docs[i])
        line_info = get_line_info(query_vector1, word_line_array[i])
        parsed_list.append((i, dot_prod, line_info))
        parsed_list = sorted(parsed_list, key=lambda x: x[1])
    return parsed_list



print()
while True:
    query = raw_input("Please enter your query....")
    if len(query) == 0:
        break
    query_list = get_tokenized_and_normalized_list(query)
    query_vector = create_vector_from_query(query_list)
    get_tf_idf_from_query_vect(query_vector)
    result_set = get_result_from_query_vect(query_vector)

    for tup in reversed(result_set) :
        if tup[1] != 0:
            print("The docid is " + str(tup[0]).zfill(4) + " and the weight is " + str(tup[1]) )
            temp = int(tup[2])
            #print (temp)
            print("Line number : ",end=' ')
            while temp !=0 :
                print(str(temp%1000) + " ",end='')
                temp = temp/1000
            print()
            print()

print()
