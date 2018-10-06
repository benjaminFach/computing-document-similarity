#  given test (query) results
#  print the doc freq and postings list
def print_test_all(term, results):
    if not print_test_freq(term, results):
        return False

    print("Posting list: ")
    print(", ".join(map(str, sorted(results.keys()))))


#  given test (query) results
#  print only the document frequency
def print_test_freq(term, results):
    print("\nTest results for {}:".format(term))

    #  if no results, print none and quit
    if results is None:
        print("No results found")
        return False

    print("{} documents returned".format(len(results.keys())))
    return True
