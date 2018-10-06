#  Imports

import fileinput
import string

from struct import pack
from utils.ingest_utils import *

#  Constants

#  a conversion table for remvoving punctuation from strings
CONV_TABLE = str.maketrans({key: None for key in string.punctuation})

#  the start of a new document, holds the doc id
START_OF_DOC = "<P ID="

#  the end of a document
END_OF_DOC = "</P>"

#  Global data structures

#  a dictionary to store results
#  key: term
#  value:  dictionary: (docID, numOccurrences)
postings_lists = dict()

#  dictionary is list of 4-tuples
#  (term, document frequency, idf, byte offset)
#
#  term: represents a word in the collection
#  document frequency: how many docs term appears in
#  idf: the inverse document frequency
#  byte offset: starting position of posting list in
#           in the inverted file

dictionary = list()

#  int to track number of unique terms
unique_terms = 0

#  int to track total number of terms
total_terms = 0

#  Document counter
document_counter = 0


# adds the term to the postings lists
def process_term(doc_id, term):
    global unique_terms
    global total_terms

    #  skip blank words, usually from a separated punctuation.
    #  Links, images too
    if is_not_term(term):
        return

    total_terms = total_terms + 1
    if term in postings_lists:
        if doc_id in postings_lists[term]:
            #  word is already in this document, increase its document occurrence
            postings_lists[term][doc_id] = postings_lists[term][doc_id] + 1
        #  word is already found in collection but new to the document
        else:
            postings_lists[term][doc_id] = 1

    #  word is new to collection
    else:
        unique_terms = unique_terms + 1
        postings_lists[term] = {doc_id: 1}


#  parse a collection
#  in this context, a file containing several "documents"
#  break into a dictionary and an inverted index
def parse_collection(collection_file, dictionary_file, inverted_index_file):
    global document_counter

    #  read in the file
    doc_id = 0

    #  check each line of file
    for line in fileinput.input([collection_file]):
        if line.startswith(START_OF_DOC):
            #  this is a new document, grab doc id from this line, do not tokenize
            doc_id = get_doc_id(line)
            document_counter = document_counter + 1

            if document_counter % 1000 == 0:
                print("Processed ", document_counter, " docs")

        elif not line.startswith(END_OF_DOC):
            line = line.translate(CONV_TABLE).rstrip().lower()
            #  this line exists in the document, append the line's tokens to the document data structure
            for token in line.split(" "):
                #if len(token) > 5:
                   #token = token[0:4]
                process_term(doc_id, token)

    #  break lexicon into a dictionary and inverted index

    #  inverted file is a sequence of bytes
    #  in the pattern of 4 bytes doc id, 4 byte term frequency
    #  this repeats until the end of the file
    inverted_file = open(inverted_index_file, 'wb')

    curr_byte_pos = 0

    #  process each term
    for term in postings_lists:
        #  based on length of posting list for term
        #  calculate number of bytes it will take
        #  in the inverted file

        dictionary.append((term, len(postings_lists[term]), curr_byte_pos))

        #  keep pointer updated
        post_byte_len = calc_post_bytes(len(postings_lists[term]))
        curr_byte_pos = curr_byte_pos + post_byte_len

        #  write all doc ids and term freq

        for doc_id in postings_lists[term]:
            inverted_file.write(pack('II', int(doc_id), int(postings_lists[term][doc_id])))

    #  sort dictionary, needed for query evaluation
    dictionary.sort()

    #  flush to disk and close inverted file opening
    #  no sort in inverted file contents!
    inverted_file.flush()
    inverted_file.close()

    with open(dictionary_file, 'w') as dict_file:
        for tup in dictionary:
            dict_file.write("{}\n".format(str(tup)))
    print(document_counter, " documents")