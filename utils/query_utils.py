import string

#  a conversion table for removing punctuation from strings
CONV_TABLE = str.maketrans({key: None for key in string.punctuation})


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