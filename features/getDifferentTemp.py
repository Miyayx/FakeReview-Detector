#!/usr/bin/env python2.7
#encoding=utf-8

"""
Read from allTemplates.dat, then process the dict to get wanted templates for further calculate
"""

from FileIO import FileIO
from vector_dict.VectorDict import VectorDict
from gensim import corpora,models,similarities

def readTemplates(filename):
    d = {}
    f = open(filename,'r')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n')
        k,v = line.split('\t\t')
        d[eval(k)] = int(v)
    f.close()
    return d

def readTempAndReview(filename):
    d = {}
    f = open(filename,'r')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n')
        k,v = line.split('\t\t')
        d[eval(k)] = eval(v)
    f.close()
    return d

def getHighFrequencyTemp(tmps,temp_review):
    templates = {}
    for k,v in tmps.items():
    # delete review with only one sent 
    # delete review with no selected template
    # delete review with only one template 
        if len(k)>1 and sum(k) > 0 and len(k)-k.count(0) >1 and k[0] != 0 and v >1:
            templates[k] = v
            print k
            for i in temp_review[k]:
                print i

    templates = sorted(templates.items(),key=lambda d:d[1],reverse=True)
    fileIO.recordToFile('highFreqTemp.dat',templates)

def VSMcalculate(tmps):
    l = []
    func = lambda t:[k for k in t if k!=0]
    for i in tmps.keys():

        for j in tmps.keys():
            # return the tuple without 0
            print dict([[k,1] for k in func(i)])
            print dict([[k,1] for k in func(j)])
            vi = VectorDict(int,dict([[k,1] for k in func(i)]))
            vj = VectorDict(int,dict([[k,1] for k in func(j)]))
            print vi
            print vj
            similiry = vi.cos(vj)
            print i
            print j
            print similiry
            l.append([i,j,similiry])

fileIO = FileIO()
if __name__=="__main__":
    templates = readTemplates('template.dat')
    temp_review = readTempAndReview('temp_and_review.dat')
    getHighFrequencyTemp(templates,temp_review)
    VSMcalculate(templates)
    

