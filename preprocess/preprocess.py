#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import os
import sys
sys.path.append("/home/yang/GraduationProject/")
from utils import fileio
from ReviewCrawler.DictUnicodeWriter import DictUnicodeWriter

def issystemreview(review):
    system_reviews = ["此用户没有填写评论!","评价方未及时做出评价,系统默认好评!","好评！"]
    if review in system_reviews:
        return True
    else: return False

def data_preprocess(review_list):
    new_review_list = []
    content_time = {}
    content_user = {}
    for item in review_list:
        if len(item) == 4:
            rid,content,user,time = item
        else:
            rid,content,time,degree,user= item[0:5]
        if issystemreview(content):
            print content
            continue
        elif len(content.decode('utf-8')) < 5:
            print content
            continue
        else:
            if content_time.has_key(content):
                if time in content_time[content] and user in content_user[content]:
                    print "timesame",content
                    continue
                else:
                    print "repilica",content
                    content_time[content].append(time)
                    content_user[content].append(user)
            else:
                content_time[content] = []
                content_time[content].append(time)
                content_user[content] = []
                content_user[content].append(user)
                new_review_list.append(item)
    return new_review_list

def remove_systemreview(review_list):
    system_reviews = ["此用户没有填写评论!","评价方未及时做出评价,系统默认好评!","好评！"]

def remove_duplicate():
    pass

def write_backto_csv(csvfile,review_list):
    fieldnames = ['id','reviewContent', 'reviewTime', 'degree','userNick', 'userId','userLink','appendId','appendReview','appendTime']
    dataL = []
    for item in review_list:
        d = {}
        for i in range(len(item)):
            d[fieldnames[i]] = item[i]
        dataL.append(d)

    with open(csvfile,"w") as f:
        dict_writer = DictUnicodeWriter(f,fieldnames,delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(dataL)

if __name__ == "__main__":
    path = "../data/CSV/Train/"
    filenames = os.listdir(path)
    for csvfile in filenames:
        review_list = fileio.read_fields_from_csv(path+csvfile)
        review_list = data_preprocess(review_list)
        write_backto_csv(path+csvfile,review_list)

