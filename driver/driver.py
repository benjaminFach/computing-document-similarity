from ingest.ingest_articles import *
from utils.query_utils import get_dictionary_from_file


#  ingest the terms into a dictionary and inverted index
parse_collection("C:/Users/Ben/data/cds14.txt", "C:/Users/Ben/data/dictionary-5stem.txt", "C:/Users/Ben/data/inverted_index-5stem")


#  grab the dictionary from file
#term_dictionary = get_dictionary_from_file("C:/Users/Ben/data/dictionary.txt")

#  grab the inverted index from file
