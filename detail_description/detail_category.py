#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import sys
import re
sys.path.append('/home/yang/GraduationProject/features/')
import fileio

TARGET_WORD_FILE = "../data/target_word.dat"
def read_target_word():
    with open(TARGET_WORD_FILE,'r') as f:
        d = {}
        while True:
            line = f.readline()
            if not line:
                break

            while not line.strip('\n').endswith('>'):
                line = f.readline()
            category = line.strip('\n').strip().strip('>')
            words = f.readline().strip('\n').split()
            d[category] = words
        return d

def get_category_count(cate_word,review):
    count = 0
    categories = ["商品","总体","小件","款式","容量","味道","内衬","材料","包装","卖家","感官","发货","物流","客服","价钱"]
    #categories = [u"总体",u"小件",u"款式",u"容量",u"味道",u"内衬",u"材料",u"包装",u"卖家"]
    others = cate_word["其他"]
    people = cate_word["人物"]
    color = re.compile(r"(?:[\u4e00-\u9fa5]*色|色差)")
    for cate in categories:
        for word in cate_word[cate]:
            if word in review:
                count += 1
    for word in others:
        if word in review:
            count += 1
    for word in people:
        if word in review:
            count += 1
            continue
    if re.match(color,review):
        count += 1
    return count

if __name__ == "__main__":
    cate_word = read_target_word()
    #for k in cate_word.keys():
    #    print k
    reviewList = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
    rid_cate = dict([rid,get_category_count(cate_word,review)] for rid,review in reviewList)
    avg = float(sum(rid_cate.values()))/len(rid_cate)
    print "avg",avg
    for rid,review in reviewList:
        print "%s\t\t%f"%(rid,rid_cate[rid]/avg)

