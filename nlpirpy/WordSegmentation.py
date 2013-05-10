#!/usr/bin/env python
#encoding=utf-8

import nlpirpy

class WordSegmentation:
    def __init__(self):
        self.strings = []

        print "You should setString or addString to add data for segmentation.\n"
        print nlpirpy.NLPIR_Init("/home/yang/GraduationProject/nlpirpy/",1)

    def setString(self,strings):
        if isinstance(strings,str):
            self.strings=[]
            self.strings.append(strings)
        if isinstance(strings,list):
            self.strings = strings

    def addString(self,strings):
        if isinstance(strings,str):
            self.strings.append(strings)
        if isinstance(strings,list):
            self.strings=self.strings+strings

    def getSegmentResultFreqDict(self):
        d = {}
        for s in self.strings:
            result = nlpirpy.NLPIR_ParagraphProcess(s.strip())
            for term in result.strip().split(' '):
                key = term.split('/')[0]
                #key = key.decode('utf-8').encode('gb2312','ignore')
                if d.has_key(key):
                    d[key] = d[key]+1
                else:
                    d[key]=1
        return d

    def getSegmentResult(self):
        l = []
        for s in self.strings:
            result = nlpirpy.NLPIR_ParagraphProcess(s.strip())
            for term in result.strip().split(' '):
                key = term.split('/')[0]
                l.append(key)
        return l

    def getSegmentResultAndRecog(self):
        l = []
        for s in self.strings:
            result = nlpirpy.NLPIR_ParagraphProcess(s.strip())
            for term in result.strip().split(' '):
                l.append(term)
        return list(set([i for i in l ]))

    def getSegmentResultAndRecogFreqDict(self):
        d = {}
        for s in self.strings:
            result = nlpirpy.NLPIR_ParagraphProcess(s.strip())
            for term in result.strip().split(' '):
                key = term
                if d.has_key(key):
                    d[key] = d[key]+1
                else:
                    d[key] = 1
        return d

    def exit(self):
        nlpirpy.NLPIR_Exit()

        
def writeToFile(filename,data):
    f = open(filename,'w')
    print data
    if isinstance(data,dict):
        for k,v in data.items():
            f.write("%s\t\t%d\n"%(k,v))
    if isinstance(data,list):
        for item in data:
            f.write(item+"\n")
    f.close()

if __name__ == '__main__':

    ws = WordSegmentation()
    ws.setString(["要去驾校考试啊","挖那么多坑是要作死啊～！"])
    
    d = ws.getSegmentResultFreqDict()
    writeToFile("test0.dat",d)
    
    l = ws.getSegmentResult()
    writeToFile("test1.dat",l)
    
    l1 = ws.getSegmentResultAndRecog()
    writeToFile("test2.dat",l1)
    
    d1 = ws.getSegmentResultAndRecogFreqDict()
    writeToFile("test3.dat",d1)
    
    ws.exit()
