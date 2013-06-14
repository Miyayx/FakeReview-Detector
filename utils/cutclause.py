#!/usr/bin/env python2.7
#encoding=utf-8

import os
import csv
import re

import fileio

remove = [u"评价方未及时做出评价",u"系统默认好评",u"`",u".",u"/",u"）",u")",u" ",u"    "]

class SentenceCutter:

    #punctuations = re.compile(r"[\"\?\|\[\]。，,！……!《》<>':：？、“”‘’；{}（）{}【】()｛｝（）：？>！。，;、~——:“”＂'\n\r]")
    #punctuations = re.compile(r"[\"\?\[\]。，,！……!':：？、“”‘’；：？！。、~——“”＂'\n\r]")
    punctuations = re.compile(r"[\?。.，,！……!：？、；：-？！、~～——\n\r\s　]|[\u3000]|\\n|<br/>|\.$|;$|&hellip;|&middot;".decode('utf-8'))
    
    def __init__(self,strings):
        self.strings = []
        if isinstance(strings,str):
            self.strings.append(strings)
        if isinstance(strings,list):
            self.strings = self.strings+strings

    def cutToClauses(self):
        allClauses = []

        for string in self.strings:
            clauses = re.split(self.punctuations,string.decode('utf-8').strip('\n'))
            for c in clauses[::-1]:
                if c == None:
                    clauses.remove(c)
                    continue
                c = c.strip("\n").strip()
                if c == u'' or len(c) == 0 or c == unicode(''): 
                    clauses.remove(c)
            allClauses.extend(clauses)

        return allClauses

    def recordToDict(self,clauses,sort = False):
        clauseFreqD = {}
        self.addToClauseDict(clauses,clauseFreqD)
        if sort:
            clauseFreqD= sorted(clauseFreqD.items(),key=lambda d:d[1],reverse=True)
        return clauseFreqD

    def addToClauseDict(self,l,d):
        for item in l:
            item = item.strip('\n').strip(' ').strip('\t')
            if item in remove:
                print item
                continue
            #print item
            if d.has_key(item):
                d[item] = d[item]+1
            else:
                d[item] = 1

if __name__=="__main__":
    csvPath = "../data/CSV/Train/"
    stringList = []
    clauseDict = {}
    filenames = os.listdir(csvPath)
    for filename in filenames:
        name = ""
        if not filename.split(".")[1] in ["csv","csv2"]:
            continue
        else:
            name = filename.split(".")[0]
        print "Cutting %s"%filename
        csvfile = csv.reader(open(csvPath+filename,'r'),delimiter="\t")
        fieldnames = csvfile.next()
        reviewIndex = fieldnames.index('reviewContent')
        appendIndex = fieldnames.index('appendReview')
        for row in csvfile:
           stringList.append(row[reviewIndex])
           stringList.append(row[appendIndex])
    

    #The code above has moved to FileIO.py
    stringList = fileio.read_fields_from_allcsv(csvPath,["reviewContent","appendReview"])

    string_list = []
    for s1,s2 in stringList:
        string_list.append(s1)
        string_list.append(s2)

    sc = SentenceCutter(string_list)
    clauseList = sc.cutToClauses()
    clauseDict = sc.recordToDict(clauseList,True)
    fileio.record_to_file('../data/preprocess/clause_dict.dat',clauseDict)
    print "finish"

    #reviews = [""]
    #sc = SentenceCutter(reviews)
    #clauseList = sc.cutToClauses()
    #for c in clauseList:
    #    print c
