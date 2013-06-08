#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from utils import fileio

def recall(target,result):
    count = 0
    all_fake = 0
    for k,v in target.items():
        if v:
            all_fake+=1
            if v == result[k]:
                count += 1
    return float(count)/all_fake

def precise(target,result):
    count = 0
    result_fake = 0
    for k,v in result.items():
        if v:
            result_fake+=1
            if v == target[k]:
                count+=1
    return float(count)/result_fake

def fvalue(precise,recall):
    return precise*recall*2/(precise+recall)

if __name__ == "__main__":
    pass

