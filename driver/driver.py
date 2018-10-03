from ingest.ingest_articles import *


#  ingest the terms into a dictionary and inverted index
parse_collection("C:/Users/Ben/data/headlines.txt", "C:/Users/Ben/data/dictionary.txt", "C:/Users/Ben/data/inverted_index")


#  grab the dictionary from file
term_dictionary = get_dictionary_from_file("C:/Users/Ben/data/dictionary.txt")

#  grab the inverted index from file
