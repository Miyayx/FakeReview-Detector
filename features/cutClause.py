#!/usr/bin/env python2.7
#encoding=utf-8

import os
import csv
import re
from FileIO import FileIO

remove = [u"评价方未及时做出评价",u"系统默认好评",u"`",u".",u"/",u"）",u")",u" ",u"    "]

class SentenceCutter:

    #punctuations = re.compile(r"[\"\?\|\[\]。，,！……!《》<>':：？、“”‘’；{}（）{}【】()｛｝（）：？>！。，;、~——:“”＂'\n\r]")
    #punctuations = re.compile(r"[\"\?\[\]。，,！……!':：？、“”‘’；：？！。、~——“”＂'\n\r]")
    punctuations = re.compile(r"[\?。，,！……!：？、；：-？！、~——\n\r\s]|\\n|<br/>|\.$|;$".decode('utf-8'))
    
    def __init__(self,strings):
        self.strings = []
        if isinstance(strings,str):
            self.strings.append(strings)
        if isinstance(strings,list):
            self.strings = self.strings+strings

    def cutToClauses(self):
        allClauses = []

        for string in self.strings:
    #        print "*******************************************"
     #       print string
            clauses = re.split(self.punctuations,string.decode('utf-8').strip('\n').strip(' '))
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


def recordToFile(filename,d):
    f = open(filename,'w')
    if isinstance(d,dict):
        for k,v in d.items():
            f.write('%s\t\t%d\n'%(k.encode('utf-8','ignore'),v))
    if isinstance(d,list):
        for k,v in d:
            f.write('%s\t\t%d\n'%(k.encode('utf-8','ignore'),v))
    f.close()

if __name__=="__main__":
    csvPath = "../data/CSV/Train/"
    stringList = []
    clauseDict = {}
    #filenames = os.listdir(csvPath)
    #for filename in filenames:
    #    name = ""
    #    if not filename.split(".")[1]=="csv2":
    #        continue
    #    else:
    #        name = filename.split(".")[0]
    #    print "Cutting %s"%filename
    #    csvfile = csv.reader(open(csvPath+filename,'r'),delimiter="\t")
    #    fieldnames = csvfile.next()
    #    reviewIndex = fieldnames.index('reviewContent')
    #    appendIndex = fieldnames.index('appendReview')
    #    for row in csvfile:
    #       stringList.append(row[reviewIndex])
    #       stringList.append(row[appendIndex])
    #
    #The code above has moved to FileIO.py
    fileIO = FileIO()
    stringList = fileIO.readReviewFromAllCSV(csvPath,["reviewContent","appendReview"])

    sc = SentenceCutter(stringList)
    clauseList = sc.cutToClauses()
    clauseDict = sc.recordToDict(clauseList,True)
    recordToFile('clauseDict.dat',clauseDict)
    print "finish"
