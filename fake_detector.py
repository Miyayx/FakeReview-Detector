#!/usr/bin/env python2.7
#encoding=utf-8

"""
This is the entrance of the whole project
"""

import ReviewClawler
import fileio

from features.cutclause import SentenceCutter as SC

def is_url(s):
    return True if s.startswith("http://") else False

def is_file(s):
    return True if s.endswith(".csv") else False

def _get_reviews_from_file(filedir):
    rid_review = fileio.read_fields_from_csv(filedir,['id','reviewContent'])
    return dict([rid,r])

def _get_reviews_from_url(url):
    r_file = ReviewClawler.main(s)
    return _get_reviews_from_file(r_file)

def _get_reviews(s):

    rid_review = {}
    if isinstance(s,list) or isinstance(s,tuple):
        for i in range(len(s)):
            rid_review[i] = s[i]
    elif isinstance(s,str):
        if is_url(s):
            rid_review = get_reviews_from_url(s)
        elif is_file(s):
            rid_review = get_reviews_from_file(s)
        else:
            rid_review[0] = s
    else:
        raise: ParameterTypeError 

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
    import urlcheck from features
    rid_url = urlcheck.url_value(rid_review)

    #Sentiment analysis
    import review_sent from sentiment_analysis
    rid_sent = review_sent.sentiment_value(rid_review)

    #General Sentence
    import reg_general from features
    rid_general = general_value(rid_review)

    #Category
    import detail_category from detail_description
    rid_cate = detail_category.category_value(rid_review)

    #Length
    import review_len from detail_description
    rid_len = review_len.length_value(rid_review)

    #Logistic regression

def fake_detect_test():
    pass

        
if __name__ == "__main__":
    fake_detect()

    
