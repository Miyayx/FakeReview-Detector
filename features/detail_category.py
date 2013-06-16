#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import sys
import re
sys.path.append('/home/yang/GraduationProject/utils/')
import fileio
from cutclause import SentenceCutter as SC

TARGET_WORD_FILE = "/home/yang/GraduationProject/data/target_word.dat"
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
    categories = ["商品","总体","小件","款式","容量","味道","内衬","材料","包装","卖家","发货","物流","客服","价钱"]
    #categories = [u"总体",u"小件",u"款式",u"容量",u"味道",u"内衬",u"材料",u"包装",u"卖家"]
    others = cate_word["其他"]
    people = cate_word["人物"]
    color = re.compile(r"(?:[\u4e00-\u9fa5]*色|色差)")
    for cate in categories:
        for word in cate_word[cate]:
            if word in review:
                count += 1
                break
    for word in others:
        if word in review:
            count += 1
    for word in people:
        if word in review:
            count += 1
            break
    if re.match(color,review):
        count += 1
    return count

def category_value(reviews):
    """
    list(list of review) -> list(list of value)
    dict(id:review) -> dict(id:value)
    string -> int
    """

    def norm(v,cnum):
        return 1 if float(v)/cnum > 1 else float(v)/cnum

    #avg = 2.4379 
    avg = float(18) 
    cate_word = read_target_word()
    if isinstance(reviews,str):
        return get_category_count(cate_word,review)/avg
    elif isinstance(reviews,list):
        cate_v = [get_category_count(cate_word,r) for r in reviews]
        #avg = float(sum(cate_v))/len(reviews)
        #return [v/avg for v in cate_v]

        clause_len = []
        for r in reviews:
            sc = SC(r)
            clause_len.append(len(sc.cutToClauses()))
        return [norm(cate_v[i],clause_len[i]) for i in range(len(reviews))]

    elif isinstance(reviews,dict):
        rid_cate = dict([rid,get_category_count(cate_word,review)] for rid,review in reviews.items())
        #avg = float(sum(rid_cate.values()))/len(rid_cate)
        #return dict([k,v/avg] for k,v in rid_cate.items())
        clause_len = {}  
        for rid,r in reviews.items():
            sc = SC(r)
            clause_len[rid] = len(sc.cutToClauses())
            if clause_len[rid] == 0:
                clause_len[rid] = 1 
        #return dict([rid,norm(rid_cate[rid],clause_len[rid])] for rid in reviews.keys()) 
        value_max = max(rid_cate.values())
        value_min = min(rid_cate.values())
        return dict([rid,(rid_cate[rid]-value_min)/float(value_max-value_min)] for rid in reviews.keys()) 
        
def category_proc(reviewobj):
    cate_word = read_target_word()
    reviewobj["category"] = get_category_count(cate_word,reviewobj["content"])
    return reviewobj["category"]
    
if __name__ == "__main__":
    reviewList = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
    rid_review = dict(reviewList)
    rid_cate = category_value(rid_review)
    for rid,value in rid_cate.items():
        #print "%s\t\t%f"%(rid_review[rid],value)
        print "%s\t\t%f"%(rid,value)

