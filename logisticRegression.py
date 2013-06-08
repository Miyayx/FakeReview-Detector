#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from sklearn import linear_model
import numpy as np

from utils import fileio
import resulttest

FEATURE_PATH="data/features/"
TARGET_PATH="data/target/"

if __name__ == "__main__":
    rid_url = fileio.read_file_to_dict(FEATURE_PATH+"url_id_feature.dat")
    rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentnorm.dict")
    #rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentratio.dict")
    rid_general = fileio.read_file_to_dict(FEATURE_PATH+"rid_general.dict")
    rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenrationorm.dict")
    #rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenratio.dict")
    rid_cate = fileio.read_file_to_dict(FEATURE_PATH+"rid_catenorm.dict")
    #rid_cate = fileio.read_file_to_dict(FEATURE_PATH+"rid_cateratio.dict")
    rid_third = fileio.read_file_to_dict(FEATURE_PATH+"rid_third.dict")
        
    fake = fileio.read_file_to_list("data/target/all_fake.dat")
    rid_fake = dict()
    for rid in rid_url.keys():
        rid_fake[rid] = 1 if rid in fake else 0
    fileio.record_to_file("data/target/rid_target.dict",rid_fake)

    trainX = []
    trainY = []
    testX = []
    testY = []
    test_id = []

    total = len(rid_url) 

    for rid in rid_url.keys()[:70000]:
        oneX = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_len[rid],rid_cate[rid]]
        #oneX = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_len[rid],rid_cate[rid],rid_third[rid]]
        #oneX = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_cate[rid]]
        trainX.append(oneX)
        trainY.append(1 if rid in fake else 0)

    trainX = np.array(trainX)
    trainY = np.array(trainY)
    print len(trainX)
    print len(trainY)
    print trainX
    print trainY

    for rid in rid_url.keys()[70000:]:
        oneX = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_len[rid],rid_cate[rid]]
        #oneX = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_len[rid],rid_cate[rid],rid_third[rid]]
        #oneX = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_cate[rid]]
        test_id.append(rid)
        testX.append(oneX)
        testY.append(1 if rid in fake else 0)

    h = .02  # step size in the mesh

    logreg = linear_model.LogisticRegression(C=1e5)

    # we create an instance of Neighbours Classifier and fit the data.
    logreg.fit(trainX, trainY)

    result = logreg.predict(testX)
    score = logreg.score(testX,testY)
    print "score",score
    print "coef_",logreg.coef_
    print "intercept_",logreg.intercept_

    #for i in range(len(result)):
    #    print testY[i],result[i]

    targetD = dict([test_id[i],testY[i]] for i in range(len(test_id)))
    #print targetD
    resultD = dict([test_id[i],list(result)[i]] for i in range(len(test_id)))
    #fileio.record_to_file("data/result/detectedid.dat",resultD.keys())
    #print resultD
    precise = resulttest.precise(targetD,resultD)
    print precise
    recall = resulttest.recall(targetD,resultD)
    print recall
    fvalue = resulttest.fvalue(precise,recall)
    print fvalue

    for k,v in resultD.items():
        if v == 1:
            print k

    
