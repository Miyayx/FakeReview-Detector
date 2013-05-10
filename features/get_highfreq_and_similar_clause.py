#!/usr/bin/env python2.7
#encoding=utf-8

"""
This program help find high frequency clause and clause with low frequency but similar with other clause,the similarity is measured by cosine distance
"""

from EditDistance import EditDistance
from FileIO import FileIO

import math
import time
from multiprocessing import Pool
from multiprocessing import Process
import multiprocessing
from collections import Counter
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean

CLAUSE_FREQ_FILE = "data/clauseDict.dat"
HIGH_FREQ_SIMIL_FILE = "data/high_freq_simil_clauses.dat"
HIGH_FREQ_FILE="data/high_freq_clauses.dat"
SIMIL_FILE = "data/simil_clauses.dat"
CALCULATED_FILE="data/temp/simil_calculated_clauses.dat"

DISTANCE = 3

def euclidean_distance(str1,str2):
    #build Vector
    iterable1 = list(str1)
    iterable2 = list(str2)
    counter1 = Counter(iterable1)
    counter2 = Counter(iterable2)
    all_items = set(counter1.keys()).union(set(counter2.keys()))
    vector1 = [counter1[k] for k in all_items]
    vector2 = [counter2[k] for k in all_items]
    #return cosine_distance
    #return cosine(vector1,vector2) 
    return euclidean(vector1,vector2) 

def has_similar(c_a,clauses):
    count = 0
    i = clauses.index(c_a)#compare from i's index, compare with clauses beside i, when length of clauses[j] is far from length of i, it's certain that there's no need to keep compareing,just stop
    offset = 1

    while True:
        if i+offset >=clause_num and i-offset < 0:
            break
        if i+offset < clause_num and len(clauses[i+offset]) - len(c_a) <=2*3:
            c_b = clauses[i+offset]
            distance = euclidean_distance(c_b,c_a) 
            if distance < DISTANCE:
                #print "\ndistance:",distance
                #print "c_b:",c_b 
                #print "c_a:",c_a
                count+=1
        if i-offset >=0 and len(c_a) - len(clauses[i-offset])<=2*3:
            c_b = clauses[i-offset]
            distance = euclidean_distance(c_b,c_a) 
            if distance < DISTANCE: 
                #print "\ndistance:",distance
                #print "c_b:",c_b 
                #print "c_a:",c_a
                count+=1
        if count >= 2 :#There are more than two clauses similar to clauses i
            #print c_a
            similar_clauses.append(c_a)
            break
        else: offset+=1

def find_similar_in_lowfreqlist(calculated_clauses,low_freq_clauses):
    low_freq_len = len(low_freq_clauses)
    low_i = 0
    process_list = []
    for c_a in low_freq_clauses[:5000]:
        low_i+=1
        print str(low_i)+"th one"
        print "-->",((low_i*100)/low_freq_len),"%"
        
        if c_a in calculated_clauses:
            continue
        #result = ppool.apply_async(has_similar,[c_a,clauses])
        p = Process(target = has_similar,name = c_a,args=(c_a,clauses))
        process_list.append(p)
        p.start()
        print "-->",p.pid,"start"
        #if result:
        #    similar_clauses.append(c_a)

    for p in process_list:
        p.join()
        print "-->",p.name,"join"
        calculated_clauses.append(p.name)

if __name__ == "__main__":
    fio = FileIO()
    calculated_clauses = [] 
    #try:
    calculated_clauses = fio.readFileToList(CALCULATED_FILE)
    #except Exception,e:
    #    print e
    #    pass

    clause_freq = fio.readFileToDict(CLAUSE_FREQ_FILE)
    clause_freq = dict([str(k),v] for k,v in clause_freq.iteritems() if len(str(k)) > 3)#clause length more than 1 chinese word
    clauses = [str(k) for k in clause_freq.keys()]
    clauses = sorted(clauses,key = lambda x:len(x))#sort clause list by clause length
    clause_num = len(clauses)
    high_freq_clauses = [str(k) for k,v in clause_freq.iteritems() if v >2]
    low_freq_clauses = [str(k) for k,v in clause_freq.iteritems() if v <=2]

    similar_clauses = fio.readFileToList(SIMIL_FILE)
    mgr = multiprocessing.Manager()
    similar_clauses = mgr.list(similar_clauses)

    try:
        find_similar_in_lowfreqlist(calculated_clauses,low_freq_clauses)
    except:
        pass
    finally:
        similar_clauses = list(similar_clauses)
        fio.recordToFile(HIGH_FREQ_FILE,high_freq_clauses)
        fio.recordToFile(SIMIL_FILE,similar_clauses)
        fio.recordToFile(HIGH_FREQ_SIMIL_FILE,set(high_freq_clauses+similar_clauses))
        fio.recordToFile(CALCULATED_FILE,calculated_clauses)
    
