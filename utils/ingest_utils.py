#  imports
import re

from nltk.corpus import stopwords

#  Constants
#  a regex pattern for extracting the document ID
DOC_ID_PATTERN = '(?<=ID=)(.*)(?=>)'

#  a set of stopwords
stop_words = set(stopwords.words('english'))


#  grab the document ID from a paragraph ID line
def get_doc_id(line):
    match = re.search(DOC_ID_PATTERN, line)
    return match.group(1)


#  check if this should count as a term
#  empty strings and hyperlinks are not terms
def is_not_term(term):
    if len(term) == 0 or term == "\n":
        return True

    elif is_link(term):
        return True

    elif term in stop_words:
        return True

    return False


#  check if this string represents a link
def is_link(term):
    if term.startswith("http") or term.endswith("jpg") or term.endswith("pdf") or term.endswith(
            "hk") or term.startswith("ctt") or term.startswith("xlinkhref") or term.startswith(
        "xlinkhref") or term.startswith("pubtypee") or term.startswith(
        "mathvariantital") or term.startswith("idnt") or term.startswith("idn0") or term.startswith(
        "idm21") or term.startswith("5ga") or term.startswith("overflowscroll") or term.startswith(
        "nc0") or term.startswith("idt") or term.startswith("idm") or term.startswith("hs00") or term.startswith(
        "gggt") or term.startswith("gctt") or term.startswith("accenttruemm"):
        return True

    return False


#  calculate number of bytes posting list will
#  take up in an inverted file
#  4 bytes for each doc id, 4 bytes for each term freq
def calc_post_bytes(post_len):
    return post_len * 8
