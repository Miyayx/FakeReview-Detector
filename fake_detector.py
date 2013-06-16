#!/usr/bin/env python2.7
#encoding=utf-8

"""
This is the entrance of the whole project
"""

from ReviewCrawler import ReviewCrawler
from utils import fileio
from utils import jsonparser

from utils.cutclause import SentenceCutter as SC
from utils.ltp.ltp_parser import LTPParser

import objective

REVIEW_LIST = []

class ParameterTypeError(Exception):
    def __init__(self,param):
        Exception.__init__(self,param)
        self.param = param
    def __str__(self):
        return "Parameter is ",self.param

def is_url(s):
    return True if s.startswith("http://") or s.startswith("https://") else False

def is_file(s):
    return True if s.find(".csv") != -1 else False

def _get_reviews_from_file(filedir):
    global REVIEW_LIST
    REVIEW_LIST = fileio.read_fields_from_csv(filedir,['id','reviewContent','userNick','reviewTime'])
    rid_review = fileio.read_fields_from_csv(filedir,['id','reviewContent'])
    return dict(rid_review)

def _get_reviews_from_url(url):
    r_file = ReviewCrawler.crawl_producturl(url)
    return _get_reviews_from_file(r_file)

def _get_reviews(s):
    rid_review = {}
    if isinstance(s,list) or isinstance(s,tuple):
        for i in range(len(s)):
            rid_review[i] = s[i]
    elif isinstance(s,str) or isinstance(s,unicode):
        if is_url(s):
            print "is_url"
            rid_review = _get_reviews_from_url(s)
        elif is_file(s):
            rid_review = _get_reviews_from_file(s)
        else:
            rid_review[0] = s
    else:
        raise ParameterTypeError(s) 
    return rid_review

review_list_obj = {}
review_obj = {}

def ltp_parse(reviewlistobj,rid_reviewobj):
    all_clauses = []
    for reviewobj in rid_reviewobj.values():
        all_clauses+=reviewobj["clauses"]
    all_clauses = set(all_clauses)
    ltp = LTPParser(all_clauses,cutted=True)
    reviewlistobj["parser_path"] = ltp.ltp_parser()

def cut_clause(string):
    sc = SC(string)
    return sc.cutToClauses()

from features import urlcheck 
from sentiment_analysis import review_sent 
from features import reg_general 
from features import detail_category 
from features import review_len 

rule_procs = [
    urlcheck.url_proc,
    reg_general.general_proc,
    detail_category.category_proc,
    review_len.length_proc,
    review_sent.sentiment_proc
]

def normalize(rid_reviewobj,feature):
    l = [obj[feature] for obj in rid_reviewobj.values()]
    Min = min(l)
    Max = max(l)
    #return [float(i-Min)/(Max-Min) for i in l]
    for reviewobj in rid_reviewobj.values():
        reviewobj[feature] = float(reviewobj[feature]-Min)/(Max-Min)

def print_reviewobj(reviewobj):
    print "=================================="
    print reviewobj["content"]
    print "url",reviewobj["url"]
    print "sentiment",reviewobj["sentiment"]
    print "general",reviewobj["general"]
    print "length",reviewobj["length"]
    print "category",reviewobj["category"]

def fake_detect_pipeline(s):
    """
    The entrance of whole project
    Parameter can be :product page url from Taobao/Tmall
                      csv file(with review information) dir
                      a review string
                      a review list

    This method use design pattern of pipeline. Use dict instead of Class. rid_reiviewobj is a dict of reviewobj, a reviewobj store all attributes it needs. reviewlistobj stores attributes needed when calculating but relative the whole review list.

    reviewobj = {
        "content":
        "url":
        "general":
        "category":
        "length":
        "sentiment":
        "clauses":
        }

    reviewlistobj = {
        "parser_path":
        "clause_xml"
        "avg_length":
        "avg_sent":
        }
    """
    try:
        rid_review = _get_reviews(s) #It's a dict, which key is id from web of review and value is content of review
    except ParameterTypeError,e:
        print e
        return

    rid_reviewobj = {}
    reviewlistobj = {}

    for rid,review in rid_review.items():
        rid_reviewobj[rid] = {}
        rid_reviewobj[rid]["content"] = review
        rid_reviewobj[rid]["clauses"] = cut_clause(review)

    ltp_parse(reviewlistobj,rid_reviewobj)

    reviewlistobj["clause_xml"] = review_sent.read_xml_to_dict(reviewlistobj["parser_path"])

    for rid in rid_reviewobj.keys():
        reviewobj = rid_reviewobj[rid]
        for proc in rule_procs[:-1]:
            proc(reviewobj)
        rule_procs[-1](reviewobj,reviewlistobj)

    avg_len = sum([obj["length"] for obj in rid_reviewobj.values()])/float(len(rid_reviewobj))

    avg_sent = sum([obj["sentiment"] for obj in rid_reviewobj.values()])/float(len(rid_reviewobj))

    for rid in rid_reviewobj.keys():
        rid_reviewobj[rid]["length"] = rid_reviewobj[rid]["length"]/avg_len
        rid_reviewobj[rid]["sentiment"] = rid_reviewobj[rid]["sentiment"]/avg_len

    normalize(rid_reviewobj,"length")
    normalize(rid_reviewobj,"sentiment")
    normalize(rid_reviewobj,"category")

    rid_target = {}
    for rid in rid_reviewobj.keys():
        reviewobj = rid_reviewobj[rid]
        print_reviewobj(reviewobj)
        #result = objective.logistic_objective(reviewobj)
        result = objective.objective(reviewobj)
        print "Result",result
        rid_target[eval(rid)] = result
    print "Review_list",len(REVIEW_LIST)

    return jsonparser.convert_to_json(REVIEW_LIST,rid_target)
        
def fake_detect(s):
    """
    The entrance of whole project
    Parameter can be :product page url from Taobao/Tmall
                      csv file(with review information) dir
                      a review string
                      a review list
    """
    try:
        rid_review = _get_reviews(s) #It's a dict, which key is id from web of review and value is content of review
    except ParameterTypeError:
        print ""
        return

    #Url checking
    rid_url = urlcheck.url_value(rid_review)
    print "rid_url",rid_url

    #Sentiment analysis
    rid_sent = review_sent.sentiment_value(rid_review)
    print "rid_sent",rid_sent

    #General Sentence
    rid_general = general_value(rid_review)
    print "rid_general",rid_general

    #Category
    rid_cate = detail_category.category_value(rid_review)
    print "rid_cate",rid_cate

    #Length
    rid_len = review_len.length_value(rid_review)
    print "rid_len",rid_len

    #Logistic regression


def fake_detect_test():
    pass

        
if __name__ == "__main__":
    reviews = [
    "很好的包包，已经第二次买了，全5分",
    "还可以，没有图片上的好看，皮质还可以的，物流也挺快的三天就到了,总体上还算挺满意得。"]
    #csvfile = "data/CSV/Train/17180958841.csv2"
    csvfile = "test.csv"
    fake_detect_pipeline(csvfile)

