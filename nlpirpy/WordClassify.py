#encoding=utf-8
import re

def writeToFile(filename,l):
    f = open(filename,'w')
    for item in l:
        f.write(item)
    f.close()

inputPath = "../data/crudeWordSeg/"
outputPath = "../data/WordSeg/"

nRex = re.compile(r'/n.*'.decode('utf-8'))
vRex = re.compile(r'/v.*'.decode('utf-8'))
aRex = re.compile(r'/a.*'.decode('utf-8'))
dRex = re.compile(r'/d.*'.decode('utf-8'))#副词

fread = open(inputPath+'all.dict','r')
nounList = []
adjList = []
advList = []
verbList = []
othersList = []

while(True):
    line = fread.readline()
    if not line:
        break
    if nRex.search(line):
        nounList.append(line)
    elif vRex.search(line):
        verbList.append(line)
    elif aRex.search(line):
        adjList.append(line)
    elif dRex.search(line):
        advList.append(line)
    else:
        othersList.append(line)

writeToFile(outputPath+'noun.dict',nounList)
writeToFile(outputPath+'verb.dict',verbList)
writeToFile(outputPath+'adj.dict',adjList)
writeToFile(outputPath+'adv.dict',advList)
writeToFile(outputPath+'others.dict',othersList)
