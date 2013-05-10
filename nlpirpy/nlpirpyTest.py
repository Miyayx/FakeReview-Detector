#!/usr/bin/env python2.7
#encoding=utf-8

"""
Test py lib nlpirpy
"""

from nlpirpy import * 
#import nlpirpy

s1 = "我在做测试。"

NLPIR_Init("",1)
result = NLPIR_ParagraphProcess(s1)
print result
print type(result)
print result.strip().split(' ')
NLPIR_Exit()

s2 = "对CNLPIR的类进行测试"
cn = CNLPIR()
result2 = cn.ParagraphProcess(s2,1)
print result2

