#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

def readFromFile(filenames):
    if isinstance(filenames,str):
        #return [line.strip().split('\t\t')[0].split('/')[0] for line in open(filename,'r')]
        return [line.strip() for line in open(filename,'r')]
    if isinstance(filenames,list):
        l = []
        for filename in filenames:
            #l = l+ [line.strip().split('\t\t')[0].split('/')[0] for line in open(filename,'r')]
            l = l+ [line.strip() for line in open(filename,'r')]
        return l

def readSentWord(filenames):
    """
    (list of str(filename)) -> list of str(word)
    """
    l = []
    for filename in filenames:
        l = l+[line.strip().decode('cp936').encode('utf-8') for line in open(filename,'r')]
    return l

def writeSettedWord(filename,method,l):
    """
    Write the assignment result to file. Different sentiment words into different files
    """
    with open(filename,method) as f:
        for i in l:
            f.write(i+'\n')

def setSentIndex(pos,neg,filename):
    """
    (list of str(positive words),list of str(negative words),str)-> dict (key:word, value:sentiment index)
    """
    words = readFromFile(filename)
    sentD = {}
    for word in words:
        if word in pos:
            sentD[word] = 1
            continue
        elif word in neg:
            sentD[word] = -1
            continue
        else:
            sentD[word] = 0
    return sentD       

def tagSentMatual(sentD):
    """
    dict of untaggedWord by hownet-> dict of all tagged words by manual and hownet
    """
    #d = dict([k,v] for k,v in sentD.iteritems if v == 0)
    for k,v in sentD.items():
        if v != 0:
            continue
        print "is %s positive or negative?"%k
        print "0:throw 1;negative 2 neutral 3 positive"
        c = raw_input(":")
        while not c in ['0','1','2','3']:
            c = raw_input(":")
        sentD[k] = int(c)-2
        

if __name__=="__main__":
    positives = readSentWord(['sentiment/正面评价词语（中文）.txt','sentiment/正面情感词语（中文）.txt'])
    negatives = readSentWord(['sentiment/负面情感词语（中文）.txt','sentiment/负面评价词语（中文）.txt'])
    sentD = setSentIndex(positives,negatives,['../data/WordSeg/new_adj.dat'])

    #sentD = {}
    #with open('../data/WordSent/neutral.dat','r') as f:
    #    sentD = dict([line.strip(),0] for line in f.readlines())
    #try:
    #    tagSentMatual(sentD)
    #finally:
    writeSettedWord('../data/WordSent2/positive.dat','a',[k for k,v in sentD.iteritems() if v == 1])
    writeSettedWord('../data/WordSent2/negative.dat','a',[k for k,v in sentD.iteritems() if v == -1])
    writeSettedWord('../data/WordSent2/neutral.dat','w',[k for k,v in sentD.iteritems() if v == 0])
    writeSettedWord('../data/WordSent2/throw.dat','a',[k for k,v in sentD.iteritems() if v == -2])


