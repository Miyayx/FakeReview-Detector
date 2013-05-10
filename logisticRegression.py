#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from sklearn import linear_model

FEATURE_PATH="data/features/"
TARGET_PATH="data/target/"

def readid2feature(filename):
    with open(filename,'r') as f:
        return dict([line.strip('\n').split('\t\t')[0],eval(line.strip('\n').split('\t\t')[1])] for line in f.readlines())

if __name__ == "__main__":
    hasUrl = readid2feature(FEATURE_PATH+"url_id_feature.dat")
    #replica = readid2feature(FEATURE_PATH+"isreplica_id_feature.dat")
    sent = readid2feature(FEATURE_PATH+"sentiment_id_feature.dat")
    #in_general_cln = readid2feature(FEATURE_PATH+"inGeneralCln_id_feature.dat")
    #detailed = readid2feature(FEATURE_PATH+"detailed_id_feature.dat")

    id_classify = readid2feature(TARGET_PATH+"rid_target.dat")
    print "Amount of fake review in train data:%d"%len([v for v in id_classify.values() if v == 1])

    id_feature_target=[]
    for k in id_classify.keys():
        try:
            id_feature_target.append([k,[hasUrl[k],sent[k]],id_classify[k]])
        except:
            print k

    X = [item[1] for item in id_feature_target]
    Y = [item[2] for item in id_feature_target]

    h = .02  # step size in the mesh

    logreg = linear_model.LogisticRegression(C=1e5)

    # we create an instance of Neighbours Classifier and fit the data.
    logreg.fit(X, Y)

    print logreg.get_params(deep=True)

    result = logreg.predict(X)
    print list(result).count(1)

