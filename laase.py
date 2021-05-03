import os
import glob
import pdftotext
import re
import math


def print_options():
    print("Please select an option from below:")
    print("1. Set directory for indexing")
    print("2. Add search category")
    print("3. Build index")
    print("4. Print index")
    print("5. Enter query")

class Posting:
    def __init__(self, doc_id, term_frequency):
        self.doc_id = doc_id
        self.term_frequency = term_frequency


search_dir = ""
doc_lex = []
doc_length = []
avg_doc_length = 1
doc_index = 0
index = dict()
term_lex = dict()
term_index = 0
postings = []
b = 0.2

def pivoted_normalization(term, query_term_count, doc_freq):
    global(index)
    global(b)
    global(avg_doc_length)
    global(doc_index)
    global(doc_length)
    score = 0
    postings = index[term]
    for posting in postings:
        first_term = (1+math.log(1+math.log(posting.term_frequency))) / ((1-b)+b * doc_length[posting.doc_id] / avg_doc_length)
        second_term = query_term_count * math.log((doc_index+1)/doc_freq)
        score += first_term * second_term

#for pivoted normalization, need doc length and avg doc length
# also need num of docs in collection (doc_index after indexing) and document frequency
# so we need to check document frequency and query frequency before running this function on each term in the query

def rank(query):
    query_terms = query.split(" ")
    #need to count how many times each term occurs and call pivoted_normalization only once for each
    #then send as an argument (query_term_count)
    #need to calculate doc_freq here for each query term

print_options()
user_choice = input()

while user_choice != "quit":
    if user_choice == "1":
        # choose directory
        search_dir = input("Enter directory: ")
    elif user_choice == "2":
        useless = 0
        # add search category
    elif user_choice == "3":
        # build index
        print("Building index . . .")
        for filename in glob.glob(os.path.join(search_dir, '*.pdf')):
            with open(filename, 'rb') as f:
                print("\tOpening", filename)
                pdf = pdftotext.PDF(f)
                sub_index = dict()
                doc_lex.append(filename)
                doc_length.append(0)
                for page in pdf:
                    #iterate over pages from pdf
                    #print(page)
                    #split into lines
                    lines = page.split("\n")
                    for line in lines:
                        #clean punctuation
                        #print(line)
                        clean_line = re.sub(r'[^\w\s]',"", line)
                        #print(clean_line)
                        words = clean_line.split(" ")
                        for word in words:
                            #need to decide how to organize everything. Take another look tomorrow and make a decision. This needs progress now
                            doc_length[doc_index] += 1
                            if word in sub_index:
                                tf = sub_index[word].term_frequency
                            else:
                                tf = 0
                            sub_index[word] = Posting(doc_index, tf + 1)
                new_dict = { key: [posting]
                             if key not in index
                             else index[key] + [posting]
                             for (key, posting) in sub_index.items() }
                index.update(new_dict)
                doc_index = doc_index + 1
        for length in doc_length:
            avg_doc_length += length
        avg_doc_length = avg_doc_length / doc_index
    elif user_choice == "4":
        # print index
        for (key, posting) in index.items():
            print(key + ":")
            for doc_posting in posting:
                print("\t"+ doc_lex[doc_posting.doc_id]+", "+ str(doc_posting.term_frequency))
    elif user_choice == "5":
        useless = 1
        # search query
    print_options()
    user_choice = input()
print("Exiting . . .")
