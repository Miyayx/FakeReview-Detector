#!/usr/bin/env python2.7
#encoding=utf-8
"""
A collection of FileIO
The all fieldnames are  
['id','reviewContent', 'reviewTime', 'degree','userNick', 'userId','userLink','appendId','appendReview','appendTime']
"""
import os
import csv
import codecs

def record_to_file(filename,data,mode='w'):
    """
    (FileIO,str,data,str) -> NoType
    str is filename
    data can be dict or list
    mode,can be 'w' or 'a'
    dict -- k:str, v:int
            k:tuple, v:int
            k:tuple, v:list
            k:int, v:str
    list -- len(item) == 1
            len(item) == 2
    """
    f = open(filename,mode)
    if isinstance(data,dict):
        for k,v in data.items():
            if isinstance(k,str) and isinstance(v,int):
                f.write('%s\t\t%d\n'%(k.encode('utf-8','ignore'),v))
            if isinstance(k,str) and isinstance(v,float):
                f.write('%s\t\t%f\n'%(k.encode('utf-8','ignore'),v))
            elif isinstance(k,tuple):
                if isinstance(v,list):
                    f.write('%s\t\t%s\n'%(k,v))
                else:f.write('%s\t\t%d\n'%(k,v))
            else:
                try:
                    f.write('%s\t\t%s\n'%(str(k),str(v)))
                except UnicodeEncodeError:
                    f.write('%s\t\t%s\n'%(k.encode('utf-8','ignore'),v.encode('utf-8','ignore')))
    elif isinstance(data,list): 
        if isinstance(data[0],list):
            if len(data[0]) == 1:
                for item in data:
                    f.write('%s\n'%str(item))
            if len(data[1]) == 2:
                for k,v in data:
                    try:
                        if isinstance(v,int):
                            f.write('%s\t\t%d\n'%(k.encode('utf-8','ignore'),v))
                        else:
                            f.write('%s\t\t%f\n'%(k.encode('utf-8','ignore'),v))
                    #except UnicodeDecodeError,AttributeError:
                    except: 
                        f.write('%s\t\t%s\n'%(str(k),str(v)))
        else:
            for item in data:
                f.write('%s\n'%str(item))

    elif isinstance(data,set):
        for item in data:
            f.write('%s\n'%str(item))
    f.close()

def read_fields_from_csv(path,filename,chosenfields):
    csvfile = csv.reader(open(path+filename,'r'),delimiter="\t")
    fieldnames = csvfile.next()
    fieldIndex = [fieldnames.index(i) for i in chosenfields]

    stringList = [[row[i] for i in fieldIndex] for row in csvfile]

    return stringList

def read_fields_from_allcsv(path,chosenfields):
    filenames = os.listdir(path)
    stringList = []
    for filename in filenames:
        name = ""
        if not filename.split(".")[1]=="csv2":
            continue
        else:
            name = filename.split(".")[0]
        stringList.extend(read_fields_from_csv(path,filename,chosenfields))
    return stringList

def read_file_to_dict(filename,reverse=False,delimiter='\t\t'):
    with open(filename,'r') as f:
        d = {}
        for l in f.readlines():
            if reverse:
                v,k = l.strip('\n').split(delimiter)
            else:k,v = l.strip('\n').split(delimiter)
            try:
                d[eval(k)]=eval(v)
            except:
                d[k] = eval(v)
    return d

def read_file_to_list(filename):
    """
    str(filename) -> list
    Read each line in the file and add each line into a list
    """
    with open(filename,'r') as f:
        return [eval(line.strip('\n')) for line in f.readlines()]

def read_templates(filename):
    """
    str(filename) -> list of tuple
    """
    with open(filename,'r') as f:
        return [eval(line) for line in f.readlines()]

