import math
import time

from ingest.ingest_articles import *

from query.query_inverted_index import query_term

from random import randint

from utils.query_utils import *
from utils.ingest_utils import *

#  Constants

#  The number of documents in the collection
NUM_DOCS = 57982

#  The number of queries being processed
NUM_QUERIES = 30

#  clock the start time
start_time = time.time()

#  ingest the terms into a dictionary and inverted index
parse_collection("S:/data/cds14.txt", "C:/Users/Ben/data/dictionary.txt", "C:/Users/Ben/data/inverted_index")

#  grab the dictionary from file
term_dictionary = get_dictionary_from_file("C:/Users/Ben/data/dictionary.txt")

#  grab the inverted index from file
index = open("C:/Users/Ben/data/inverted_index", 'rb')

#  a dictionary to store document lengths
#  key: document ID
#  value: length
document_lengths = dict()

#  look up each term in the inverted index
for term in term_dictionary:
    #  look up the term by querying for it
    #  query returns a dictionary in the form...
    #  key: doc ID
    #  value: term freq
    term_info = query_term(term, term_dictionary, index)

    #  do processing for each document this term appears in
    idf = math.log2(NUM_DOCS / len(term_info))
    for doc in term_info:
        tf = term_info[doc]
        tf_idf = tf * idf

        #  store the square of tf-idf in accumulator
        if doc in document_lengths:
            document_lengths[doc] = document_lengths[doc] + (tf_idf ** 2)
        else:
            document_lengths[doc] = (tf_idf ** 2)

#  to get the length, need to take the square root of these sum of squares
for length in document_lengths:
    document_lengths[length] = math.sqrt(document_lengths[length])

#  process the query document
queries = get_queries_from_file("C:/Users/Ben/data/cds14.topics.txt")

#  process each query
for query_id in queries:
    #  store the query as a map of term to term frequency
    #  key: term
    #  value: number of occurrences in the query
    query_map = dict()

    #  store the tf-idf vector
    query_tf_idf_vector = list()

    #  store the tf-idf's as a map of document to tf-idf
    #  this is populated by progressing through query terms
    #  key: document id
    #  value: tf-idf vector (a fixed length array, size = size of query)
    document_tf_idf_vectors = dict()

    #  hold the vector length of the query
    query_vector_length = 0

    for term in queries[query_id].split(" "):
        #  tokenize query in same manner as document indexing

        #  skip blank words, usually from a separated punctuation.
        #  Links, images too
        if is_not_term(term):
            continue

        # if len(term) > 5:
        # term = term[0:4]

        # if is_not_term(term):
        # continue

        if term in query_map:
            query_map[term] = query_map[term] + 1

        else:
            query_map[term] = 1

    # print("Query as a bag of words: {}".format(query_map))

    #  generate a ranked list of document results for each query

    #  do calculations one query term at a time
    curr_query_index = 0
    idf = 0
    for term in query_map:
        query_term_info = query_term(term, term_dictionary, index)

        #  tf for query comes from query
        tf = query_map[term]

        #  idf for query comes from background documents
        idf = math.log2(NUM_DOCS / len(query_term_info))
        tf_idf = tf * idf

        #  build query tf-idf vector
        query_tf_idf_vector.append(tf_idf)

        #  also update the query vector length
        query_vector_length = query_vector_length + (tf_idf ** 2)

        #  query has been handled, now process documents that contain this term
        for doc in query_term_info:
            tf = query_term_info[doc]
            doc_tf_idf = tf * idf

            #  initialize vector if this is a newly discovered document
            if doc not in document_tf_idf_vectors:
                document_tf_idf_vectors[doc] = [0] * len(query_map)
                document_tf_idf_vectors[doc][curr_query_index] = doc_tf_idf

            #  otherwise just place the tf-idf in the correct place
            else:
                document_tf_idf_vectors[doc][curr_query_index] = doc_tf_idf

        curr_query_index = curr_query_index + 1

    #  once terms have been traversed, finalize the query vector length by taking square root of sum of squares
    query_vector_length = math.sqrt(query_vector_length)

    print("Query as a vector: {}".format(query_tf_idf_vector))

    #  calculate a score for each document
    #  store results in a dictionary of the form:
    #  key: cosine_score
    #  value: list[query_id, "Q0", doc_id, rank (inserted after sort), cosine_score, fach]
    results = dict()
    for document in document_tf_idf_vectors:
        dot_prod = sum([a * b for a, b in zip(query_tf_idf_vector, document_tf_idf_vectors[document])])
        lengths_prod = query_vector_length * document_lengths[document]
        if lengths_prod == 0:
            cosine_score = 0
        else:
            cosine_score = "%.6f" % round(dot_prod / lengths_prod, 6)

        #  add a random string to make sure index is unique if happen to have same cosine score
        results["{}-{}".format(cosine_score, randint(0, 99999999))] = [query_id, "Q0", document,
                                                                       cosine_score, "fach"]

    #  sort by key, insert rank, then output to file
    #  cut off at 100
    sorted_results = (sorted(results.keys(), reverse=True))
    final_results = []
    count = 0
    for key in sorted_results:
        count = count + 1
        if count > 100:
            break
        final_results.append(results[key])

    rank = 1
    with open("C:/Users/Ben/data/cosine_cds14_output.txt", "a+") as out:
        print(" ".join(["q_id", "str", "doc_id", "rank", "score", "name"]))
        print("\n")
        for result in final_results:
            result.insert(3, rank)
            out.write(" ".join(str(element) for element in result))
            out.write("\n")
            rank = rank + 1

print("Execution took {} seconds".format(time.time() - start_time))
print("Vocabulary size: {}".format(len(term_dictionary)))
