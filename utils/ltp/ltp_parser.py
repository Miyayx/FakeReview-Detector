#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import os
import sys
import codecs
import convert_coding

sys.path.append('/home/yang/GraduationProject/utils')
from cutclause import SentenceCutter as SC

SENTENCE_FILE = "/home/yang/GraduationProject/data/parser/ltp_parser_sentence.dat"
PARSER_RESULT = "/home/yang/GraduationProject/data/parser/ltp_parser_result_utf8.dat"

class LTPParser:
    """
    Use LTP to parse review sentence. 
    Write the result to data/parser
    """

    def __init__(self,strs,cutted=False):
        self.str_list = []
        if isinstance(strs,str):
            self.str_list.append(strs)
        if isinstance(strs,list) or isinstance(strs,set):
            self.str_list+=strs
        if not cutted:
            clauses = self._cut()
        else: clauses = self.str_list
        self._write_to_file(clauses)

    def _write_to_file(self,clauses):
        with codecs.open(SENTENCE_FILE,'w','gb2312') as f:
            for c in clauses:
                try:
                    f.write(c+"\n")
                except:
                    print c

    def _cut(self):
        sc = SC(self.str_list)
        clauses = sc.cutToClauses()
        return clauses
        
    def ltp_parser(self):
        os.system("sh /home/yang/GraduationProject/ltp/bin/ltp_test.sh")
        convert_coding.convert_encoding(PARSER_RESULT,"utf-8")
        return PARSER_RESULT


if __name__ == "__main__":
    review = "这是我见过的最好看的包了"
    ltp = LTPParser(review)
    ltp.ltp_parser()
