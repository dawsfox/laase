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
doc_score = []
avg_doc_length = 1
doc_index = 0
index = dict()
term_lex = dict()
term_index = 0
b = 0.2

def pivoted_normalization(term, query_term_count):
    global index
    global b
    global avg_doc_length
    global doc_index
    global doc_length
    global doc_score
    doc_freq = 0
    postings = index[term]
    for posting in postings:
        #calculate document frequency
        doc_freq = doc_freq + 1
    for posting in postings:
        first_term = (1+math.log(1+math.log(posting.term_frequency))) / ((1-b)+b * doc_length[posting.doc_id] / avg_doc_length)
        second_term = query_term_count * math.log((doc_index+1)/doc_freq)
        doc_score[posting.doc_id] += first_term * second_term

#for pivoted normalization, need doc length and avg doc length
# also need num of docs in collection (doc_index after indexing) and document frequency
# so we need to check document frequency and query frequency before running this function on each term in the query

def rank(query):
    global doc_index
    #initialize scores to zero
    for i in range(doc_index):
        doc_score[i] = 0
    query_terms = query.split(" ")
    query_one = []
    for qt in query_terms:
        if qt not in [item[0] for item in query_one]:
            query_one.append((qt, 1))
        else:
            for (match, freq) in query_one:
                if (match == qt):
                    freq = freq + 1
    for (qt, qt_freq) in query_one:
        pivoted_normalization(qt, qt_freq)
    return

def retrieve(ret_count):
    high_score = 0
    top_index = 0
    for i in range(ret_count):
        for j in range(doc_index):
            if doc_score[j] > high_score:
                high_score = doc_score[j]
                top_index = j
        print(str(i+1)+".) "+doc_lex[top_index]+" with score "+str(high_score))
        #set retrieved article's score to 0 to avoid reprinting it
        doc_score[top_index] = 0
        top_index = 0
        high_score = 0
    return

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
                doc_score.append(0)
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
        # search query
        query = input("Please enter a query: ")
        rank(query)
        retrieve(5)
    print_options()
    user_choice = input()
print("Exiting . . .")
