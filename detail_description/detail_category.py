#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import sys
import re
sys.path.append('/home/yang/GraduationProject/features/')
from FileIO import FileIO

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
    categories = [u"商品",u"总体",u"小件",u"款式",u"容量",u"味道",u"内衬",u"材料",u"包装",u"卖家",u"感官",u"发货",u"物流",u"客服",u"价钱"]
    #categories = [u"总体",u"小件",u"款式",u"容量",u"味道",u"内衬",u"材料",u"包装",u"卖家"]
    color = re.compile(ur"[\u4e00-\u9fa5]+色")
    for cate in categories:
        for word in cate_word[cate.encode('utf-8')]:
            if word in review:
                count += 1
                break
    if re.match(color,review):
        count += 1
    return count

if __name__ == "__main__":
    cate_word = read_target_word()
    #for k in cate_word.keys():
    #    print k
    fio = FileIO()
    reviewList = fio.readFieldsFromAllCSV("../data/CSV/Train/",["id","reviewContent"])
    rid_cate = dict([rid,get_category_count(cate_word,review)] for rid,review in reviewList)
    avg = float(sum(rid_cate.values()))/len(rid_cate)
    print "avg",avg
    for rid,review in reviewList:
        print "%s\t\t%f"%(rid,rid_cate[rid]/avg)

