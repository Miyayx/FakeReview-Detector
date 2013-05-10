#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from xml.dom.minidom import parse,parseString
import sys
import os
import codecs
import matplotlib.pyplot as plt
import numpy as np
sys.path.append('/home/yang/GraduationProject/features/')
from FileIO import FileIO 
from ltpXML import ltpXML
from cutClause import SentenceCutter as SC
 
sentWordPath = '../data/WordSent/'
fio = FileIO() 
pos_adj = fio.readFileToList(sentWordPath+'positive.dat')
neg_adj = fio.readFileToList(sentWordPath+'negative.dat')
neg_adv = fio.readFileToList(sentWordPath+'negative_adv.dat')
adv_degree = fio.readFileToDict(sentWordPath+'adv_degree.dat')

XML_FILE="../data/parser/all_clause_parse_utf8.dat"

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
                f.readline()
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
        except:
            pass

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
        print "adv degree:",adv_degree[adv.encode('utf-8')]
        return adv_degree[adv.encode('utf-8')]
    else: return 1

def calculate_clause_sent(c_ltp):
    relate_str = c_ltp.get_clause_relate_path()
    if relate_str in subject_paths:
        return 0
    elif "SBV" in c_ltp.relate_list and c_ltp.word_list[c_ltp.relate_list.index('SBV')] in ['赞','贊']:
        return 1
    else:
        if "ADV@HED" in relate_str:
            hed_i = c_ltp.relate_list.index('HED')
            adv_i = hed_i -1
            hed_w = c_ltp.word_list[hed_i]
            adv_w = c_ltp.word_list[adv_i]

            polar = sent_polar(hed_w)
            adv_degree = get_adv_degree(adv_w)

            return polar*adv_degree
        elif "ADV@DE" in relate_str and "DE" in c_ltp.relate_list:
            adv_i = c_ltp.relate_list.index('ADV')
            de_i = c_ltp.relate_list.index('DE')
            adv_w = c_ltp.word_list[adv_i]
            de_w = c_ltp.word_list[de_i]

            polar = sent_polar(de_w)
            adv_degree = get_adv_degree(adv_w)

            return polar*adv_degree
        elif "HED" in relate_str:
            hed_i = c_ltp.relate_list.index('HED')
            hed_w = c_ltp.word_list[hed_i]
            polar = sent_polar(hed_w)
            return polar
        else: return 0

REVIEW_PATH = "../data/CSV/Train/"
FEATURE_PATH = "../data/features/"
if __name__ == "__main__":
    clause_xml = read_xml_to_dict(XML_FILE)
    #for clause,xml_str in clause_xml.iteritems():
    #    c_ltp = ltpXML(clause,xml_str)
        #print clause,calculate_clause_sent(c_ltp)
    review_sentratio = {}
    rid_sentratio = {}
    filenames = os.listdir(REVIEW_PATH)
    for filename in filenames:
        name = ""
        if not filename.split(".")[1] == "csv2":
            continue
        else:
            name = filename.split(".")[0]
        reviewList = fio.readFieldsFromCSVToList(REVIEW_PATH,filename,["id","reviewContent"])
        rid_sent = dict([rid,calculate_review_sent(clause_xml,review)] for rid,review in reviewList)    
        review_sent = dict([review,rid_sent[rid]] for rid,review in reviewList)
        avg_sent = float(sum(rid_sent.values()))/len(rid_sent)
        rid_sentratio.update(dict([k,v/avg_sent] for k,v in rid_sent.iteritems()))
        review_sentratio.update(dict([k,v/avg_sent] for k,v in review_sent.iteritems()))

    fio.recordToFile(FEATURE_PATH+"rid_sentratio.dict",rid_sentratio)

    for k,v in review_sentratio.items():
        print k,v

