#encoding=utf-8
import re
import time

import sys
sys.path.append("/home/yang/GraduationProject/utils/")
import fileio

def has_url(review):
    #urlRexExp = re.compile('([a-zA-Z]+|{[0-9]+[a-zA-Z]+}+[a-zA-Z]*|{[a-zA-Z]+[0-9]+}+[0-9]*)\.[a-z0-9-A-Z]+'.decode('utf-8'))
    #urlRexExp = re.compile(r'[a-zA-Z]+[0-9]*\.[a-z0-9-A-Z]+'.decode('utf-8'))
    urlRexExp = re.compile(r'\.com|\.net|\.cn|\.COM|\.CN|\.NET|QQ|Q群'.decode('utf-8'))#re.l忽略大小写
    spaceExp = re.compile(r'\s')
    return True if urlRexExp.search(spaceExp.sub('',review).lower()) else False

def url_proc(reviewobj):
    reviewobj["url"] = int(has_url(reviewobj["content"]))

def url_value(reviews):
    if isinstance(reviews,str):
        return int(has_url(reviews))
    elif isinstance(reviews,list):
        return [int(has_url(r)) for r in reviews]
    elif isinstance(reviews,dict):
        return dict([k,int(has_url(r))] for k,r in reviews.items())

if __name__ == "__main__":
    
    #fileio.record_to_file("../data/features/url_id_feature.dat",d)

    review_list = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
    rid_review = dict(review_list)
    rid_url = dict([rid,int(has_url(review))] for rid,review in rid_review.iteritems())
    fileio.record_to_file("../data/new_features/rid_url.dict",rid_url)

