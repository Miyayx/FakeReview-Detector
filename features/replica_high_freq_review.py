#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
sys.path.append('/home/yang/GraduationProject/')

from utils import fileio

DATA_FILE = "../data/preprocess/"

if __name__ == "__main__":
    high_freq_temp = fileio.read_file_to_dict(DATA_FILE+"highFreqTemp.dat")
    temp_rid = fileio.read_file_to_dict(DATA_FILE+"temp_and_rid.dat")
    high_freq_list = []

    for temp in high_freq_temp.keys():
        high_freq_list.extend(temp_rid[temp])

    #print high_freq_list
    for item in high_freq_list:
        print item
    print len(high_freq_list)
