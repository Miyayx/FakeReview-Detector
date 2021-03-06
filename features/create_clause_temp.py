#!/usr/bin/env python2.7
#encoding=utf-8

import sys
sys.path.append("/home/yang/GraduationProject/utils/")
from cutclause import SentenceCutter
import fileio

RECORD_PATH = "../data/preprocess/"

def readClauseFromFile(filename):
    """
    str(filename)-> list of str(subClause)
    """
    l=[]
    f = open(RECORD_PATH+'clause_dict.dat','r')
    while(True):
        line = f.readline()
        if not line:
            break
        k,v = line.strip('\n').split('\t\t')
        if int(v) < 2:
            continue
        l.append(k)
    f.close()
    return l

def setIdToClause(l):
    d = {}
    for item in l:
        d[item] = l.index(item)+1
    return d 

def readAllClauseFromFile(filename):
    with open(filename,'r') as f:
        return [line.strip('\n').split('\t\t')[0] for line in f.readlines()]

def template_process():
    clauseList = readClauseFromFile(RECORD_PATH+'clause_dict.dat') 
    allClause = readAllClauseFromFile(RECORD_PATH+'clause_dict.dat')
    print len(clauseList)
    clauseIdDict = setIdToClause(clauseList)
    fileio.record_to_file(RECORD_PATH+'clauseIdDict.dat',[(k,clauseList.index(k)+1) for k in clauseList])
    fileio.record_to_file(RECORD_PATH+'allClause_id.dat',[(k,allClause.index(k)+1) for k in allClause])
    fileio.record_to_file(RECORD_PATH+'all_clauses.dat',allClause)
    reviewList = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent","reviewTime"])
    temps = {} 
    id_Temp = {}
    for r_id,review,t in reviewList:
        sc = SentenceCutter(review)
        clauses = sc.cutToClauses()
        Temp = tuple([allClause.index(c.encode('utf-8'))+1 for c in clauses if c.encode('utf-8') in allClause ])
        temp=tuple([clauseList.index(c.encode('utf-8'))+1 if c.encode('utf-8') in clauseList else 0 for c in clauses])
        # create a dict without recording time
        #if templates.has_key(temp):
        #    templates[temp] = templates[temp]+1
        #else: templates[temp] = 1

        # create a dict with time, time and frequency are in a list as dict value
        if temps.has_key(temp):
            if temps[temp]['time'] == t:
                continue
            temps[temp]['freq'] = temps[temp]['freq']+1
            temps[temp]['reviews'].append(review)
            temps[temp]['review_id'].append(r_id)
        else:
            temps[temp] = {'time':t,'freq':1,'reviews':[review],'review_id':[r_id]}

        id_Temp[r_id] = Temp
    print "finish cut"
    #k=template, v=frequence
    freqfunc = lambda d:dict([[k,v['freq']] for k,v in d.iteritems() ])
    #k=template, v= list of review
    reviewfunc = lambda d:dict([[k,v['reviews']] for k,v in d.iteritems() ])
    #k=template, v= list of review id
    idfunc = lambda d:dict([[k,v['review_id']] for k,v in d.iteritems()])
    #write all template into file
    freqtemps = freqfunc(temps)
    fileio.record_to_file(RECORD_PATH+'allTemplates.dat',sorted(freqtemps.items(),key=lambda d:d[1],reverse=True))

    fileio.record_to_file(RECORD_PATH+'all_id_temp.dat',sorted(id_Temp.items(),key=lambda d:d[0]))

    #define a filter which help remove the template with little suspect
    #choose the ones which have more than two sentence and not all of them are unique(appear only once) and has at least two no unique sentences
    #delete the template which have too many unique sentence
    def f(x):
        zeroNum = x.count(0)
        return len(x) > 2 and sum(x) > 0 and len(x)-zeroNum > 1 and float(zeroNum)/(len(x) -zeroNum) < 2

    #get matching templates
    filteredTmps = filter(f,temps.keys())
    newtemps = dict((k,v) for k,v in temps.iteritems() if k in filteredTmps)
    
    #get a dict which k = template and v = reviewlist
    reviewtemps = reviewfunc(newtemps)
    fileio.record_to_file(RECORD_PATH+'temp_and_review.dat',reviewtemps)

    #get a dict which k = template and v = idlist
    idtemps = idfunc(newtemps)
    fileio.record_to_file(RECORD_PATH+'temp_and_rid.dat',idtemps)
    replicaId = []
    for k,v in idtemps.items():
        print k,v
        if len(v)>1:
            replicaId+=v
    fileio.record_to_file(RECORD_PATH+'replicaId.dat',replicaId)

    templates = freqfunc(newtemps)
    templates = sorted(templates.items(),key=lambda d:d[1],reverse=True)
    fileio.record_to_file(RECORD_PATH+'template.dat',templates)
    
    highfreq = dict((k,v) for k,v in templates if v > 1)
    highfreq= sorted(highfreq.items(),key=lambda d:d[1],reverse=True)
    fileio.record_to_file(RECORD_PATH+'highFreqTemp.dat',highfreq)
    
    #Sort the templates by its length(the review's length)
    lengthSorted = sorted(newtemps.keys(),key=lambda x:len(x),reverse = True)
    fileio.record_to_file(RECORD_PATH+'lengthSortedTemp.dat',lengthSorted)
    
    print "done"


if __name__=="__main__":
    #template_process()
    newtemps = fileio.read_file_to_dict(RECORD_PATH+"template.dat")
    lengthSorted = sorted(newtemps.keys(),key=lambda x:len(x),reverse = True)
    print lengthSorted
    fileio.record_to_file(RECORD_PATH+'lengthSortedTemp.dat',lengthSorted)

