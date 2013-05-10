#encoding=utf-8
import csv
import json
import os
import codecs
import sys
from WordSegmentation import WordSegmentation

inputPath = "../data/CSV/Train/"
outputPath = "../data/nlpirCrudeWordSeg/"

def writeToFile(filename,data):
    f = open(filename,'w')
    if isinstance(data,dict):
        for k,v in data.items():
            f.write("%s\t\t%d\n"%(k,v))
    if isinstance(data,list):
        for k,v in data:
            f.write("%s\t\t%d\n"%(k,v))
    f.close()

filenames = os.listdir(inputPath)
ws = WordSegmentation()
stringList = []
for filename in filenames:
    name = ""

    if not filename.split(".")[1] == "csv2":
        continue
    else:
        name = filename.split(".")[0]

    print "Cutting %s"%filename
    csvfile = csv.reader(codecs.open(inputPath+filename,'r'),delimiter="\t")
    fieldnames = csvfile.next()
    
    contentIndex = fieldnames.index('reviewContent')
    appendIndex = fieldnames.index('appendReview')

    #stringList = []
    for row in csvfile:
        content = row[contentIndex]
        stringList.append(content)
        if len(row[appendIndex]) == 0:
            stringList.append(row[appendIndex])

ws.setString(stringList)
d = ws.getSegmentResultAndRecogFreqDict()
sortedD = sorted(d.items(),key=lambda d:d[1],reverse=True)
writeToFile(outputPath+"all.dict",sortedD)
ws.exit()
