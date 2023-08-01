import math
import json
import itertools
import re
class RankedDocs:
    def q_index(self,query):
        query_words = query.split(" ")
        q_termfreq = {}
        for i in query_words:
            if i not in q_termfreq:
                q_termfreq[i] = 1
            else:
                q_termfreq[i] += 1
        return q_termfreq
    def term_weights(self, tf):
        # print(tf)
        term_weights_dict = {}
        for i in tf:
            if tf[i] != 0:
                term_weights_dict[i] = 1 + round(math.log10(tf[i]), 4)
            else:
                 term_weights_dict[i] = 0
        return term_weights_dict
    def calc_document_frequency(self, doc_freq, tf):
        qword_d_frequency = {}
        for i in tf:
            if i in doc_freq:
                qword_d_frequency[i] = doc_freq[i]
        return qword_d_frequency
    def calc_logfreq(self, doc_freq, N):
        logtf_dictionary = {}
        for i in doc_freq:
            logtf_dictionary[i] =1 + round(math.log10(N/doc_freq[i]),4 )  
        return logtf_dictionary  
    def euclidean_dist(self, vals):
        e_dist = 0
        for i in vals:
            e_dist +=  vals[i]**2
        e_dist = math.sqrt(e_dist)
        normalized_vectors = {}
        for i in vals:
            normalized_vectors[i] = round(vals[i]/e_dist, 4)
        return normalized_vectors
    def log_termfreq(self, tf, idf):
        log_tf_dict = {}
        for i in tf:
            log_tf_dict[i] = tf[i]*idf[i]
        return log_tf_dict
    def cosine_score(self, doc_score, query_score):
        score = 0
        for i in doc_score:
            score += doc_score[i]*query_score[i]
        return score
    def calc_tf_idf(self,tf, doc_freq, N):
        term_weights_dict = self.term_weights(tf)
        # print("tf-weight",term_weights_dict)
        qword_d_frequency = self.calc_document_frequency(doc_freq,tf)
        # print("doc freqency",qword_d_frequency)
        logtf_dictionary = self.calc_logfreq(qword_d_frequency,N)
        # print("idf-weight",logtf_dictionary)
        tf_idf = self.log_termfreq(term_weights_dict, logtf_dictionary)
        # print("tf-idf-weight",tf_idf)
        tf_idf_norm = self.euclidean_dist(tf_idf)
        # print("tf_idf-weight",tf_idf_norm)
        return tf_idf_norm


docs_retrieval = RankedDocs()

N = 1000
f = open('newinverted.json',"r")
data = json.load(f)
f.close()
query = ""
q_num=0
while query != "quit":
    query = ""
    query_postings = {}
    if query == "":
        query = input("please enter your query : ")
        q_num+=1
        if query == "quit":
            break
    # q_num = input("please enter the query number: ")

    q = query.lower()
    q_tf = docs_retrieval.q_index(q)
    # print(q_tf)

    words_list = len(q_tf)
    words_notfound= 0
    for word in q_tf:
        try:
            query_postings[word] = data[word]
        except:
            # print(word, " not in the inverted index, please check the spelling")
            words_notfound += 1
            # q_num-=1
    
    if words_notfound == words_list:
        q_num -=1
      
    # print(str(q_num))
    f.close()
    iquery_tf ={}
    for word in query_postings:
        iquery_tf[word] = q_tf[word]
        

    # print("query posting list : ")
    # print(query_postings)

    merged_lists = []
    for word in query_postings:
        for i in query_postings[word]['postings']:
            if i["doc"] not in merged_lists:
                merged_lists.append(i["doc"])
    # print("merged posting list : ",merged_lists)     

    docs_tf = {}
    for doc in merged_lists:
        doc_tf  = {}
        f = open('News_Dataset/{}.txt.txt'.format(str(doc).zfill(4)), encoding='utf8')
        # f = open("News_Dataset/"+doc+".txt", encoding="utf8")
        lines = f.read()
        c = re.sub('([^a-zA-Z0-9+])', " ", lines)
        f.close()
        idoc_tf = docs_retrieval.q_index(c.lower())
        for word in idoc_tf:
            if word in data:
                doc_tf[word] = idoc_tf[word]
        docs_tf[doc] = doc_tf
    cosine_scores = {}
    for doc in merged_lists:
        # print()
        # print(doc)
        query_tf = {}
        for word in docs_tf[doc]:
            if word in iquery_tf:
                query_tf[word] = iquery_tf[word]
            else:
                query_tf[word] = 0
        doc_freq = {}
        for word in query_tf:
            sum = 0
            for i in data[word]['postings']:
                sum += int(i["freq"])
            doc_freq[word] = sum
        # print(doc_freq)
        tf_idf_query = docs_retrieval.calc_tf_idf(query_tf, doc_freq, N)
        tf_idf_doc = docs_retrieval.calc_tf_idf(docs_tf[doc], doc_freq, N)

        # print(tf_idf_query,tf_idf_doc)
        cosine_score = docs_retrieval.cosine_score(tf_idf_doc, tf_idf_query)
        # print("cosine score",cosine_score)
        cosine_scores[doc] = cosine_score
        
    ranked_docs = {}

    ranked_docs = {k: v for k, v in sorted(cosine_scores.items(), key=lambda item: item[1])}
    final_ranked_docs = {}


    rank = 0
    for i in reversed(ranked_docs):
        doc = {}
        rank += 1
        doc["score"] = cosine_scores[i]
        doc["rank"] = rank
        final_ranked_docs[i] = doc
    print()
    print("final ranked documents") 
    for i in final_ranked_docs:
        print(i, final_ranked_docs[i])
        
    sample = {}
    try:
        sample = dict(itertools.islice(final_ranked_docs.items(), 10)) 
    except:
        sample = dict(itertools.islice(final_ranked_docs.items(), 10)) 
    
    # Writing to sample.json
    ret = {}
    if str(q_num) != "1":
        with open("ranked_retrieved.json") as infile:
            ret = json.load(infile)
            ret[str(q_num)] = sample
            ret = json.dumps(ret, indent=4)
        with open("ranked_retrieved.json", "w") as outfile:
            outfile.write(ret)
    else:
        with open("ranked_retrieved.json", "w") as outfile:
            ret[str(q_num)] = sample
            outfile.write(json.dumps(ret, indent=4))
            

    # Relevance Feedback

    relevant_docs = {}
    if str(q_num) != "1":
        with open("relevance.json") as infile:
            relevant_docs = json.load(infile)
    else:
        relevant_docs = {}

    relevant_list = []
    for i in sample:
        relevance = int(input("Is Document {doc} relevant to your query? if it is relevant enter 1, if not enter 0: ".format(doc = i)))
        if relevance == 1:
            relevant_list.append(i)

    relevant_docs[str(q_num)] = relevant_list

    with open("relevance.json", "w") as outfile:
        relevant = json.dumps(relevant_docs, indent=4)
        outfile.write(relevant) 
    