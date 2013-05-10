#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

inputPath = '../data/WordSeg/'
outputPath = '../data/WordSeg/'

#inputFile = 'adj.dict'
inputFile = 'noun.dict'

def writeToFile(path,filename,l):
    with open(path+filename,'w') as f:
        for i in l:
            f.write(i+"\n")
try:
    newadj = [w.strip('\n') for w in open(inputPath+'new_adj.dat','r')]
    newnoun =[w.strip('\n') for w in open(inputPath+'new_noun.dat','r')]
    newother = [w.strip('\n') for w in open(inputPath+'new_other.dat','r')]
    theme = [w.strip('\n') for w in open(inputPath+'theme.dat','r')]
    print len(newadj)
    print len(newnoun)
    print len(newother)

    n = 0
    for word in open(inputPath+inputFile,'r'):
        word = word.strip().split('\t\t')[0].split('/')[0]
        n +=1
        if (word in newadj) or (word in newnoun) or (word in newother) or (word in theme):
            continue
        print "No.",n
        #print "Is %s adj?"%word
        #print "Enter:yes 1:noun 2:nothing"
        print "Is %s a theme?"%word
        print "Enter:yes 1:normal noun 2:adj 3:nothing"
        c = raw_input(":")
        if not len(c):
            theme.append(word)
        elif int(c)==1:
            newnoun.append(word)
        elif int(c)==2:
            newadj.append(word)
        else: newother.append(word)

finally:
    writeToFile(outputPath,'theme.dat',set(theme))
    writeToFile(outputPath,'new_adj.dat',set(newadj))
    writeToFile(outputPath,'new_noun.dat',set(newnoun))
    writeToFile(outputPath,'new_other.dat',set(newother))
    
