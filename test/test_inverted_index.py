from utils.testing_utils import *
from utils.query_utils import get_dictionary_from_file

from query.query_inverted_index import query_term

#  open inverted index for retrieval
index = open("C:/Users/Ben/data/inverted_index", 'rb')

#  get the dictionary from file
term_dictionary = get_dictionary_from_file("C:/Users/Ben/data/dictionary.txt")

#  doc freqs and postings list
print_test_all("oxygen", query_term("oxygen", term_dictionary, index))
