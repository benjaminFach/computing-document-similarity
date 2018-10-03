#  imports
import re

#  a regex pattern for extracting the document ID
DOC_ID_PATTERN = '(?<=ID=)(.*)(?=>)'


#  grab the document ID from a paraph ID line
def get_doc_id(line):
    match = re.search(DOC_ID_PATTERN, line)
    return match.group(1)


#  check if this should count as a term
#  empty strings and hyperlinks are not terms
def is_not_term(term):
    if len(term) == 0 or term == "\n" or is_link(term):
        return True

    return False


#  check if this string represents a link
def is_link(term):
    if term.startswith("http") or term.endswith("jpg") or term.endswith("pdf") or term.endswith("hk"):
        return True

    return False


#  calculate number of bytes posting list will
#  take up in an inverted file
#  4 bytes for each doc id, 4 bytes for each term freq
def calc_post_bytes(post_len):
    return post_len * 8
