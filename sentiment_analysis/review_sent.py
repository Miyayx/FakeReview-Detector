#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from xml.dom.minidom import parse,parseString
import sys
import os
import codecs
import numpy as np

sys.path.append('/home/yang/GraduationProject/utils/')
import fileio 
from cutclause import SentenceCutter as SC
from ltp.ltp_xml import ltpXML
from ltp import ltp_parser

sentWordPath = '/home/yang/GraduationProject/data/WordSent/'
pos_adj = fileio.read_file_to_list(sentWordPath+'positive.dat')
neg_adj = fileio.read_file_to_list(sentWordPath+'negative.dat')
neg_adv = fileio.read_file_to_list(sentWordPath+'negative_adv.dat')
adv_degree = fileio.read_file_to_dict(sentWordPath+'adv_degree.dat',delimiter=None)

subject_paths = ["ADV@ADV@HED@MT","ADV@HED@VOB@MT","ADV@POB@HED@MT","HED@VOB@VOB@MT","QUN@ADV@ADV@HED@MT","QUN@ATT@HED","DE@VOB@HED","HED@SBV@DE@ATT@VOB","HED@MT@QUN@VOB@MT","QUN@HED","HED@CMP@MT","HED@MT@QUN@VOB","ADV@HED@MT@QUN@VOB","QUN@ADV@HED@MT"]

def read_xml_to_dict(xml_file):
    """
    str->dict(sentence,xmlstring)
    """

    with codecs.open(xml_file,'r','utf-8') as f:
        d = {}
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith('Input'):
                clause = line.strip('\n').split(': ',2)[1]
                while(not f.readline().startswith("Result")):
                    continue
                xml_string = ""
                xml_line = ""
                while(not xml_line.startswith("</xml4nlp>")):
                    xml_line = f.readline()
                    xml_string += xml_line
                d[clause.encode('utf-8')] = xml_string.encode('utf-8')
        return d
    
def calculate_review_sent(clause_xml,review):
    """
    str -> int(index of sentiment)
    """

    sc = SC(review)
    clause_list = sc.cutToClauses()

    r_sent = 0
    for clause in clause_list:
        try:
            c_ltp = ltpXML(clause,clause_xml[clause.encode('utf-8')])
            r_sent += calculate_clause_sent(c_ltp)
        except KeyError,e:
            print e
    return r_sent

def sent_polar(word):
    if word in pos_adj:
        return 1
    elif word in neg_adj:
        return -1
    else: return 0

def get_adv_degree(adv):
    if adv in neg_adv:
        return -1
    elif adv in adv_degree.keys():
        #print "adv degree:",adv_degree[adv.encode('utf-8')]
        return adv_degree[adv.encode('utf-8')]
    else: return 1

def calculate_clause_sent(c_ltp):

    def get_polar(relate):
        word_i = c_ltp.relate_list.index(relate)
        word = c_ltp.word_list[word_i]
        #print "polar word",word
        return sent_polar(word)
    def get_degree(relate):
        word_i = c_ltp.relate_list.index(relate)
        word = c_ltp.word_list[word_i]
        #print "adv word",word
        return get_adv_degree(word)
        
    relate_str = c_ltp.get_clause_relate_path()
    #print relate_str
    #print c_ltp.sentence
    if relate_str in subject_paths:
        return 0
    elif "SBV" in c_ltp.relate_list and c_ltp.word_list[c_ltp.relate_list.index('SBV')] in ['赞','贊']:
        return 1
    else:
        if "ADV@ADV@HED" in relate_str:
            #print "if ADV@ADV@HED"
            hed_i = c_ltp.relate_list.index('HED')
            adv_i2 = hed_i -1
            adv_i1 = hed_i -2

            hed_w = c_ltp.word_list[hed_i]
            adv_w1 = c_ltp.word_list[adv_i1]
            adv_w2 = c_ltp.word_list[adv_i2]

            ##print hed_w
            #print adv_w1
            #print adv_w2

            polar = sent_polar(hed_w)
            adv_degree1 = get_adv_degree(adv_w1)
            adv_degree2 = get_adv_degree(adv_w2)
            if polar*adv_degree1*adv_degree2 != 0:
                #print polar*adv_degree1*adv_degree2
                return polar*adv_degree1*adv_degree2

        adv_and_word = ["ADV@HED","ADV@VOB","ADV@VV","HED@CMP"]

        for sub_relate in adv_and_word:
            if sub_relate in relate_str: 
                #print sub_relate 
                adv_r,word_r = sub_relate.split("@")
                word_i = c_ltp.relate_list.index(word_r)
                adv_i = word_i -1
                word_w = c_ltp.word_list[word_i]
                adv_w = c_ltp.word_list[adv_i]

                polar = sent_polar(word_w)
                adv_degree = get_adv_degree(adv_w)

                #print "adv",adv_w
                #print "word",word_w
                if polar*adv_degree != 0:
                    #print polar*adv_degree
                    return polar*adv_degree

        if "ADV@DE" in relate_str and "DE" in c_ltp.relate_list:
            #print "if ADV@DE"

            adv_i = c_ltp.relate_list.index('ADV')
            de_i = c_ltp.relate_list.index('DE')
            adv_w = c_ltp.word_list[adv_i]
            de_w = c_ltp.word_list[de_i]
            #print adv_w
            #print de_w

            polar = sent_polar(de_w)
            adv_degree = get_adv_degree(adv_w)

            if polar*adv_degree != 0: 
                #print polar*adv_degree
                return polar*adv_degree

        if "HED@VOB" == relate_str:
            #print "if HED@VOB"
            hed_i = c_ltp.relate_list.index('HED')
            vob_i = c_ltp.relate_list.index('VOB')
            hed_w = c_ltp.word_list[hed_i]
            vob_w = c_ltp.word_list[vob_i]

            adv_degree = 1
            polar = sent_polar(vob_w)
            if polar == 0:
                polar = sent_polar(hed_w)
            else:
                adv_degree = get_adv_degree(hed_w)

            #print hed_w
            #print vob_w

            if polar*adv_degree != 0:
                #print polar*adv_degree
                return polar*adv_degree

        if "HED" in relate_str:
            #print "if HED"
            hed_i = c_ltp.relate_list.index('HED')
            hed_w = c_ltp.word_list[hed_i]
            polar = sent_polar(hed_w)

            #print hed_w

            if polar != 0:
                #print polar
                return polar
        if "VOB" in relate_str:
            #print "if VOB"
            vob_i = c_ltp.relate_list.index('VOB')
            vob_w = c_ltp.word_list[vob_i]
            polar = sent_polar(vob_w)
            #print vob_w
            #if polar != 0:
                #print polar
        if "VV" in relate_str:
            #print "if VV"
            vv_i = c_ltp.relate_list.index('VV')
            vv_w = c_ltp.word_list[vv_i]
            polar = sent_polar(vv_w)

            #print vv_w
            #if polar != 0:
                #print polar

        return 0

def average(l):
    avg = 1.688
    if len(l) > 0:
        avg = sum(l)/float(len(l))
        if avg == 0:
            avg = 1.688
    return avg

def sentiment_value(reviews,xml_file=None):
    """
    list(list of review) -> list(list of value)
    dict(id:review) -> dict(id:value)
    string -> int
    """
    if not xml_file:
        if isinstance(reviews,dict):
            ltp = ltp_parser.LTPParser(reviews.values())
        else:
            ltp = ltp_parser.LTPParser(reviews)
        ltp.cut()
        ltp.ltp_parser()
        xml_file = ltp_parser.PARSER_RESULT

    avg = 1.688 
    clause_xml = read_xml_to_dict(xml_file)

    if isinstance(reviews,str):
        return abs(calculate_review_sent(clause_xml,reviews)-avg)/avg

    elif isinstance(reviews,list):
        sent_v = [calculate_review_sent(clause_xml,r) for r in reviews]
        avg = average(sent_v)
        return [abs(v-avg)/avg for v in sent_v]
        return sent_v

    elif isinstance(reviews,dict):
        rid_sent = dict([rid,calculate_review_sent(clause_xml,review)] for rid,review in reviews.items())
        avg = average(rid_sent.values())
        return dict([k,abs(v-avg)/avg] for k,v in rid_sent.items())
        return rid_sent

def sentiment_proc(reviewobj,reviewlistobj):
    clause_xml = reviewlistobj["clause_xml"]
    reviewobj["sentiment"] = calculate_review_sent(clause_xml,reviewobj["content"])
    return reviewobj["sentiment"]


REVIEW_PATH = "../data/CSV/Train/"
#FEATURE_PATH = "../data/features/"
FEATURE_PATH = "../data/new_features/"

def calculate_sentvalue():

    #XML_FILE="../data/parser/all_clause_parse_utf8.dat"
    XML_FILE="../data/preprocess/all_clause_parse_utf8.dat"
    review_sentratio = {}
    rid_sentratio = {}
    rid_sentnorm = {}

    filenames = os.listdir(REVIEW_PATH)
    for filename in filenames:
        name = ""
        if not filename.split(".")[1] in ["csv2","csv"]:
            continue
        else:
            name = filename.split(".")[0]
        reviewList = fileio.read_fields_from_csv(REVIEW_PATH+filename,["id","reviewContent"])
        reviewdict = dict(reviewList)
        temp_rid_sentratio = sentiment_value(reviewdict,XML_FILE)
        review_sentratio.update(dict([reviewdict[k],v] for k,v in temp_rid_sentratio.iteritems()))

        ratio_max = max(temp_rid_sentratio.values())
        ratio_min = min(temp_rid_sentratio.values())

        rid_sentratio.update(temp_rid_sentratio)
        rid_sentnorm.update(dict([k,(v-ratio_min)/(ratio_max-ratio_min)] for k,v in temp_rid_sentratio.iteritems()))

    fileio.record_to_file(FEATURE_PATH+"rid_sentratio.dict",rid_sentratio)
    fileio.record_to_file(FEATURE_PATH+"rid_sentnorm.dict",rid_sentnorm)

    #for k,v in review_sentratio.items():
    #    print k,v

    #print sum(review_sentratio.values())/float(len(review_sentratio))


if __name__ == "__main__":

    XML_FILE="../data/parser/all_clause_parse_utf8.dat"
    #review_sentratio = {}
    #rid_sentratio = {}

    #reviews = ["包很好，非常喜欢！ 挺好"]
    #reviews = "质量非常好，与卖家描述的完全一致，非常满意<br/>\
    #   卖家的服务太棒了，考虑非常周到，完全超出期望值<br/>\
    #    卖家发货速度非常快，包装非常仔细、严实<br/>\
    #        物流公司服务态度很好，运送速度很快<br/>"

    #sentratio = sentiment_value(reviews,XML_FILE)     

    #print reviews,sentratio

    calculate_sentvalue()

    #print calculate_review_sent(read_xml_to_dict(XML_FILE),"所有同事都说太好看了这款~皮质也很软。重要的是双十一能够这么快到货，着实是个惊喜~谢谢亲 祝生意兴隆！")
    
