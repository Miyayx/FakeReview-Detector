#!/usr/bin/env python2.7
#encoding=utf-8

import sys
sys.path.append("/home/yang/GraduationProject/utils/")
import fileio
from cutclause import SentenceCutter as SC

TARGET_WORD_FILE = "/home/yang/GraduationProject/data/target_word.dat"
def get_third_word():
    with open(TARGET_WORD_FILE,'r') as f:
        d = {}
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith("人物"):
                words = f.readline().strip('\n').split()
                return words

def third_people(thirds,review):
    sc = SC(review)
    clauses = sc.cutToClauses()
    def func(first,second,string):
        #string = review.partition(first)[2]
        #string= string.decode('utf-8')
        #string = string[0:min(20,len(string))]
        for word in second:
            if word.decode('utf-8') in string:
                print word
                print string.encode('utf-8')
                return 1

    words = ["买","说好","拍","说不错"]
    for c in clauses:
        if u"推荐" in c:
            if func("推荐",thirds,c):
                return 1
        if u"介绍" in c:
            if func("介绍",thirds,c):
                return 1
        for people in thirds:
            if people.decode('utf-8') in c:
                if func(people,words,c):
                    return 1
    return 0

if __name__=="__main__":
    review_list = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
    thirds = get_third_word()
    #review = "包包很大气，适合的年龄段很宽，皮质很软，很高贵，而且卖家服务态度非常好，发货和到货后都来信息提示，包装也非常仔细，说预售5天发货，但三天就货了，而 且发货速度非常给力，同事还有很多要买的，祝老板生意兴隆。"
    #print third_people(thirds,review)
    rid_third = dict([rid,third_people(thirds,review)] for rid,review in review_list)
    fileio.record_to_file("../data/features/rid_third.dict",rid_third)

