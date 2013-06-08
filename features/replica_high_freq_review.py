#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
sys.path.append('/home/yang/GraduationProject/')

from utils import fileio

if __name__ == "__main__":
    high_freq_temp = fileio.read_file_to_dict("data/highFreqTemp.dat")
    temp_rid = fileio.read_file_to_dict("data/temp_and_rid.dat")
    high_freq_list = []

    for temp in high_freq_temp.keys():
        high_freq_list.extend(temp_rid[temp])

    print high_freq_list
    print len(high_freq_list)
