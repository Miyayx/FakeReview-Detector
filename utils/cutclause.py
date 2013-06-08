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
    #        print "*******************************************"
     #       print string
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
    #stringList = fileio.read_fields_from_allcsv(csvPath,["reviewContent","appendReview"])

    #string_list = []
    #for s1,s2 in stringList:
    #    string_list.append(s1)
    #    string_list.append(s2)

    #sc = SentenceCutter(string_list)
    #clauseList = sc.cutToClauses()
    #clauseDict = sc.recordToDict(clauseList,True)
    #fileio.record_to_file('clauseDict.dat',clauseDict)
    #print "finish"

    reviews = ["先和卖家说声抱歉.评价的晚了.但我还是要说.这款包包真是大爱啊.超好看.质量一级棒.几乎没有味道.看着很小里面真的好能装东西.超喜欢.","对不起对不起收到货就放长假了一直没想起来..包包质量一级棒..没臭味做工又精细..一直不敢尝试这个颜色怕不够正会显得廉价..但看到实物超满意哈哈哈","包到了就迫不及待的背上了&middot;&middot;很好看那&middot;&middot;&middot;颜色很很正&middot;&middot;内衬很可爱&middot;&middot;卖家贴心的包装很满意&middot;&middot;赠送的卡套也超级可爱&middot;&middot;&middot;&middot;很喜欢&middot;&middot;全五分&middot;&middot;以后要是买包&middot;&middot;就认准小象啦&middot;&middot;物美价廉&middot;&middot;&middot;","很漂亮的一款包包～很喜欢哦～最喜欢花纹图案～朋友们都喜欢外表带子的款式～很精致～除了两边那两条带子的作工不是很满意～其他的还好～就是戴的时候会有点利～其他都很满意～会介绍朋友来哦～","不好意思确认晚了&hellip;宝贝皮很软&hellip;挺好看的&hellip;但是为嘛老是被折进去样子好心痛&hellip;再挺一点更好了&hellip;但是还是物美价廉而且卖家态度好好"]
    sc = SentenceCutter(reviews)
    clauseList = sc.cutToClauses()
    for c in clauseList:
        print c
