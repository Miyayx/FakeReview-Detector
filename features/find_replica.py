#!/usr/bin/env python2.7
#encoding=utf-8

"""
Find replicate review by checking if it's in line with the template
"""

import fileio 

if __name__ == '__main__':
    import os
    # get the total amount of clause which appear more than once
    #total = os.popen("wc -l %s "%(inputPath+clauseFile)).readline().split(' ')[0]
    #total = int(total)+1

    temp_freq = fileio.read_file_to_dict('data/template.dat')
    temp_freq = dict([k,v] for k,v in temp_freq.iteritems() if v > 1)

    temp_rid = fileio.read_file_to_dict('data/temp_and_rid.dat')

    duprid = []
    for temp in temp_freq.keys():
        duprid = duprid+temp_rid[temp]

    for rid in duprid:
        print rid


