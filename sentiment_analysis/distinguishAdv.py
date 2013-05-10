#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
inputAdv = "../data/WordSeg/adv.dict"
path = "../data/WordSent/"

def readAdvFromFile(filename):
    if isinstance(filename,str):
        return [line.strip().split('\t\t')[0].split('/')[0] for line in open(filename,'r')]

def readListFromFile(filename):
    with open(filename,'r') as f:
        return [line.strip() for line in f.readlines()]

def writeToFile(filename,l):
    with open(filename,'w') as f:
        for i in l:
            f.write(i+"\n")

if __name__ == "__main__":
    adv = readAdvFromFile(inputAdv)
    print len(adv)
    try:
        degreeAdv = readListFromFile(path+'degree_adv.dat')
        negAdv = readListFromFile(path+'negative_adv.dat')
        notAdv = readListFromFile(path+'not_adv.dat')
    except:
        degreeAdv = []
        negAdv = []
        notAdv = []
    print len(degreeAdv)
    print len(negAdv)
    print len(notAdv)
    try:
        for i in adv:
            if i in degreeAdv or i in negAdv or i in notAdv:
                continue
            print i
            print "1 degree adv  2 negative adv"
            c = raw_input(":")
            if len(c) == 0:
                notAdv.append(i)
            elif int(c) == 1:
                degreeAdv.append(i)
            elif int(c) == 2:
                negAdv.append(i)
    finally:
        writeToFile(path+'degree_adv.dat',degreeAdv)
        writeToFile(path+'negative_adv.dat',negAdv)
        writeToFile(path+'not_adv.dat',notAdv)


