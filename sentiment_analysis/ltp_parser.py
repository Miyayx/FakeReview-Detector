#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import os
import sys
import codecs
import convert_coding

sys.path.append('/home/yang/GraduationProject/features/')
from cutclause import SentenceCutter as SC

SENTENCE_FILE = "../data/parser/ltp_parser_sentence.dat"
PARSER_RESULT = "../data/parser/ltp_parser_result.dat"

class LTPParser:
    """
    Use LTP to parse review sentence. 
    Write the result to data/parser
    """

    def __init__(self,strs):
        self.str_list = []
        if isinstance(strs,str):
            self.str_list.append(strs)
        if isinstance(strs,list):
            self.str_list+=strs

    def cut(self):
        sc = SC(self.str_list)
        clauses = sc.cutToClauses()
        with open(SENTENCE_FILE,'w') as f:
            for c in clauses:
                f.write(c.encode('utf-8')+"\n")
        
    def ltp_parser(self):
        os.system("../ltp/bin")
        os.system("./ltp_test all %s > %s"%(SENTENCE_FILE,PARSER_RESULT))
        convert_coding.convert_encoding(PARSER_RESULT,"utf-8")


if __name__ == "__main__":
    review = "这是我见过的最好看的包了"
    ltp = LTPParser(review)
    ltp.cut()
    ltp.ltp_parser()
