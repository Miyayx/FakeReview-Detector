#!/usr/bin/env python2.7
#encoding=utf-8

"""
This is the entrance of the whole project
"""

import ReviewClawler
import fileio

def is_url(s):
    return True if s.startswith("http://") else False

def main(s):
    if is_url(s):
        review_file = ReviewClawler.main(s)
        FileIO.read
    


    
