import string
from struct import unpack

#  constants
BYTE_LEN = 8
ID_LEN = 4
FREQ_LEN = 4

#  a conversion table for removing punctuation from strings
CONV_TABLE = str.maketrans({key: None for key in string.punctuation})


#  given a term, return the doc ids
#  and term freqs
def query_term(term, dictionary, index):
    #  dict data structure for storing results
    #  key: doc ID
    #  value: term freq
    results = dict()

    #  apply same rules to query as indexing
    term = term.translate(CONV_TABLE).rstrip().lower()

    #  grab byte offset from dictionary
    try:
        byte_offset = int(dictionary[term][1])

    except KeyError:
        return None

    #  move file pointer to this offset
    index.seek(byte_offset)

    #  we need to read 8 bytes for each doc
    #  4 byte doc id, 4 byte term freq
    doc_count = int(dictionary[term][0])

    for i in range(0, doc_count * BYTE_LEN, BYTE_LEN):
        doc_id = unpack('I', index.read(ID_LEN))[0]
        term_freq = unpack('I', index.read(FREQ_LEN))[0]
        results[doc_id] = term_freq

    return results
