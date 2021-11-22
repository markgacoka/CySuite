from itertools import islice

def print_wordlist(wordlist_path, N):
    with open(wordlist_path) as myfile:
        head = list(islice(myfile, N))
    yield(head)