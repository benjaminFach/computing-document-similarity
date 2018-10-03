from utils.testing_utils import *
from utils.query_utils import get_dictionary_from_file

from query.query_inverted_index import query_term

#  open inverted index for retrieval
index = open("C:/Users/Ben/data/inverted_index", 'rb')

#  get the dictionary from file
term_dictionary = get_dictionary_from_file("C:/Users/Ben/data/dictionary.txt")

#  doc freqs and postings list
print_test_all("Heidelberg", query_term("Heidelberg", term_dictionary, index))
print_test_all("plutonium", query_term("plutonium", term_dictionary, index))
print_test_all("Omarosa", query_term("Omarosa", term_dictionary, index))
print_test_all("octopus", query_term("octopus", term_dictionary, index))

#  doc freq only
print_test_freq("Hopkins", query_term("Hopkins", term_dictionary, index))
print_test_freq("Harvard", query_term("Harvard", term_dictionary, index))
print_test_freq("Stanford", query_term("Stanford", term_dictionary, index))
print_test_freq("college", query_term("college", term_dictionary, index))

#  Jeff Bezos test
jeff_results = query_term("Jeff", term_dictionary, index)
bezos_results = query_term("Bezos", term_dictionary, index)
jeff_bezos_test = {x: jeff_results[x] for x in jeff_results if x in bezos_results}
print_test_all("Jeff Bezos", jeff_bezos_test)
