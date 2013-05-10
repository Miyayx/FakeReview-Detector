#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from FileIO import FileIO

inputPath='data/'
tempFile='lengthSortedTemp.dat'

if __name__== "__main__":
    fileIO = FileIO()
    tempL = fileIO.readTemplates(inputPath+tempFile)
