import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import json
import statistics

average_precision = []

rec = []
def recall(retrieved, relevant):
    totalRet = 0
    for i in retrieved:
        for j in range(len(relevant)):
            if i == relevant[j]:
                totalRet += 1
        val = list(retrieved.keys()).index(i) + 1
        print('Recall at', val, 'is:',  totalRet / float(len(relevant)))
        rec.append(totalRet / float(len(relevant)))


prec = []
def precision(retrieved, relevant):
    totalRet = 0
    for i in retrieved:
        for j in range(len(relevant)):
            if i == relevant[j]:
                totalRet += 1
        val = list(retrieved.keys()).index(i) + 1
        print('Precision at', val, 'is:', totalRet / float(val))
        prec.append(totalRet / float(val))


def F1(prec, rec):
    f1_score = 0.0
    for i in range(len(prec)):
        if(rec[i]==0.0 and prec[i] == 0.0):
            f1_score =  0.0
            print("F1 score at", i+1, "is : ", f1_score)
        
        else:
            f1_score = ((2*(prec[i])*(rec[i]))/(prec[i] + rec[i]))
            print("F1 score at", i+1, "is : ", f1_score)
        f1_score = 0.0



ret = {}
with open("ranked_retrieved.json") as infile:
    ret = json.load(infile)
    
relevant = {}
with open("relevance.json") as infile:
    relevant = json.load(infile)
    
for i in ret:
    print(i)
    print("For Query {query}: ".format(query = i))
    recall(ret[i], relevant[i])
    print()
    precision(ret[i], relevant[i])


    F1(rec,prec)

    # Average Precision for query i
    sum_q = 0.0
    for j in range(len(prec)):
        sum_q = sum_q + prec[j]
        
    print(i)
    averagep_q = sum_q/(len(relevant[i]))
    print("The average precison for Query {query} is : ".format(query = i), averagep_q)
    average_precision.append(averagep_q)

    # Plotting PR curve query i
    plt.plot(rec, prec)
    plt.title('Precision-Recall curve for Query{query}'.format(query = i))
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.grid()
    plt.savefig('precision-recall curve for query{query}.png'.format(query = i))
    plt.show()

    rec.clear()
    prec.clear()

    print()
    

meanap = statistics.mean(average_precision)
print("The Mean Average Precision for the {i} queries is : ".format(i = len(ret)), meanap)