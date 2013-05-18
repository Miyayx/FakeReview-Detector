#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
sys.path.append('/home/yang/GraduationProject/features/')
import fileio

adv_degree = fileio.read_file_to_dict("../data/WordSent/adv_degree.dat",delimiter=None)
adv_degree = sorted(adv_degree.items(),key = lambda x:x[1],reverse = True)

for k,v in adv_degree:
    print "%s\t\t%f"%(k,v)

