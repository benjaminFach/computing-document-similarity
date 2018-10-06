import re
import string

#  Constants

#  the start of a new document, holds the doc id
START_OF_QUERY = "<Q ID="

#  the end of a document
END_OF_QUERY = "</Q>"

#  a regex pattern for extracting the query ID
QUERY_ID_PATTERN = '(?<=ID=)(.*)(?=>)'

#  a conversion table for removing punctuation from strings
CONV_TABLE = str.maketrans({key: None for key in string.punctuation})

#  Utility functions

#  grabs the query ID from an identifier
def get_query_id(line):
    match = re.search(QUERY_ID_PATTERN, line)
    return match.group(1)


#  load in dictionary from file and return
#  each line is tuple
#  (term, document frequency, byte offset)
def get_dictionary_from_file(file_name):
    term_dict = dict()
    with open(file_name, "r") as dictionary_file:
        for tup in dictionary_file:
            entry = tup[1:-1].split()
            key = entry[0].translate(CONV_TABLE).rstrip().lower()
            val = (entry[1][0:-1], entry[2][:-1])
            term_dict[key] = val
    return term_dict

#  parse a document containing queries
#  return as a dictionary in the form of:
#  key: query ID
#  value: query (string representation)
def get_queries_from_file(file_name):
    queries = dict()
    query_id = 0
    with open(file_name, "r") as query_file:
        for line in query_file:
            if line.startswith(START_OF_QUERY):
                query_id = get_query_id(line)

            elif not line.startswith(END_OF_QUERY) and len(line) > 0 and not line == "\n":
                line = line.translate(CONV_TABLE).rstrip().lower()

                #  add to dictionary holding query IDs and query text
                if query_id in queries:
                    queries[query_id] = queries[query_id] + " " + line

                else:
                    queries[query_id] = line

    return queries
