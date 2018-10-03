#  Imports

import string
from utils.ingest_utils import *
from struct import pack

#  Constants

#  a conversion table for removing punctuation from strings
CONV_TABLE = str.maketrans({key: None for key in string.punctuation})

#  Global data structures

#  a dictionary to store results
#  key: term
#  value:  dictionary: (docID, numOccurences)
postings_lists = dict()

#  dictionary is list of 3-tuples
#  (term, document frequency, byte offset)
#
#  term: represents a word in the collection
#  document frequency: how many docs term appears in
#  byte offset: starting position of posting list in
#           in the inverted file

dictionary = list()

#  int to track number of unique terms
unique_terms = 0

#  int to track total number of terms
total_terms = 0

#  Document parser

#  reads a document and gets each term
#  by splitting on space and adds the term to the postings lists
def process_document_content(doc_id, document):
    global total_terms
    global unique_terms

    terms = document.split(" ")
    for term in terms:
        term = term.translate(CONV_TABLE).rstrip().lower()

        #  skip blank words, usually from a separated punctuation.
        #  Links, images too
        if is_not_term(term):
            continue

        total_terms = total_terms + 1
        if term in postings_lists:
            if doc_id in postings_lists[term]:
                #  word is already in this document, increase its document occurence
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
    #  read in the file
    current_line = 0
    doc_id = 0
    with open(collection_file, 'r') as headlines:
        for line in headlines:
            current_line = current_line + 1

            #  document ID is the first line
            if current_line % 4 == 1:
                doc_id = get_doc_id(line)

            #  document content is the second, process for each term
            elif current_line % 4 == 2:
                process_document_content(doc_id, line)

            #  third and fourth lines are closed p tags and empty lines

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