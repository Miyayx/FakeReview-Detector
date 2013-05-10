#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

def readListFromFile(filename):
    """
    str -> list of str
    """
    with open(filename,'r') as f:
        return [line.strip('\n') for line in f.readlines()] 

def readDictFromFile(filename):
    """
    str -> dict 
    """
    with open(filename,'r') as f:
        d = {}
        for line in f.readlines():
            k,v = line.strip().split('\t\t')
            try:
               k = eval(k)
            except:
               pass
            try:
               v = eval(v)
            except:
               pass
            d[k] = v
        return d

def recordToFile(filename,data):
    """
    (str,data) -> NoType
    str is filename
    data can be dict or list
    dict -- k:str, v:int
            k:tuple, v:int
            k:tuple, v:list
    list -- len(item) == 1
            len(item) == 2
    """
    f = open(filename,'w')
    if isinstance(data,dict):
        for k,v in data.items():
            if isinstance(k,str):
                f.write('%s\t\t%d\n'%(k,v))
            if isinstance(k,tuple):
                if isinstance(v,list):
                    f.write('%s\t\t%s\n'%(k,v))
                else:f.write('%s\t\t%d\n'%(k,v))
            else: f.write('%s\t\t%s\n'%(str(k),str(v)))
    if isinstance(data,list):
        if isinstance(data[0],list):
            if len(data[0]) == 1:
                for item in data:
                    f.write('%s\n'%str(item))
            if len(data[1]) == 2:
                for k,v in data:
                    try:
                        f.write('%s\t\t%d\n'%(k,v))
                    #except UnicodeDecodeError,AttributeError:
                    except AttributeError:
                        f.write('%s\t\t%d\n'%(k,v))
                    except TypeError:
                        f.write('%s\t\t%s\n'%(k,v))
                    except UnicodeDecodeError:
                        f.write('%s\t\t%d\n'%(k,v))
        else:
            for item in data:
                f.write('%s\n'%str(item))
    f.close()

