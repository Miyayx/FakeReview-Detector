#!/usr/bin/env python2.7
#encoding=utf-8

"""
In this module, use scikit-learn module to culter the templates.
To culter is to gether the similar templates.
Use DBSCAN algorithm
"""
import time
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn import preprocessing
from scipy import sparse

from FileIO import FileIO

inputPath='data/'
ouputPath = 'data/'
#inputFile='temp_and_id.dat'
inputFile='lengthSortedTemp.dat'
clauseFile='clauseIdDict.dat'
TEMP_ID_FILE='temp_and_rid.dat'

#Turn templates into vector
def turnTemplateToVector(t,total):
    """
    (tuple(template),int(total of clauses)) -> list of int (appear frequence )
    """
    indice = set(t)
    l = [0 for i in range(total)]
    for i in indice:
        l[i]+=1
    return l

def turnTemplateToDict(t):
    """
    tuple(template) -> dict of (int,int) (clause id and frequence)
    """
    d = {}
    for i in t:
        d[i]=d.get(i,1)+1
    return d

def mergeTmpInCluster(c):
    """
    list of tuple(template) -> tuple(more genenic template)
    rule:retain clause id that templates have in common,retain the minimax frequence
    """
    dicts = [turnTemplateToDict(i) for i in c]
    func = lambda x,y:dict([k,min(x.get(k,0),y.get(k,0))] for k in x.keys()+y.keys())
    d = dicts[0]
    for i in range(1,len(c)):
        d = func(d,dicts[i])

    if d.has_key(0):
        del d[0]

    return dict([k,v] for k,v in d.iteritems() if v > 0)

if __name__ == '__main__':
    import os
    # get the total amount of clause which appear more than once
    total = os.popen("wc -l %s "%(inputPath+clauseFile)).readline().split(' ')[0]
    total = int(total)+1
    fio = FileIO()
    templates = fio.readTemplates(inputPath+inputFile)
    temp_rids = fio.readFileToDict(inputPath+TEMP_ID_FILE)
    #print templates[0:3]
    #lb = preprocessing.LabelBinarizer()
    #X = lb.fit_transform(templates)
    #X = [turnTemplateToVector(t,total) for t in templates]
    #print type(X)
    #print len(X)
    #print type(X[0])
    #print len(X[0])
    start = time.time()
    rowN = len(templates)
    mtx = sparse.lil_matrix((rowN,total))
    for i in range(rowN):
        mtx[i,:] = turnTemplateToVector((templates[i]),total)
    print time.time()-start
    print mtx.getnnz()
    print mtx.shape[0]
    
    db = DBSCAN(eps=1.8,min_samples=2).fit(mtx.toarray()[10000:])
    core_samples = db.core_sample_indices_
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print db
    print labels
    print core_samples
    replicaId = []
    for i in core_samples:
        print i,templates[i]
        replicaId+=temp_rids[(templates[i])]
    print n_clusters_

    #arrange samples into a list of cluster
    clusters = [[] for i in range(n_clusters_)]
    for i in range(len(labels)):
        cluster_no = int(labels[i])
        if cluster_no != -1:
            clusters[cluster_no].append(templates[i])
    print clusters
    
    #merge templates in one cluster into a more generic template
    genericTmp = [mergeTmpInCluster(c) for c in clusters]
    print "\n"
    print genericTmp

    fio.recordToFile('data/generic_tmp2.dat',genericTmp)
    fio.recordToFile('data/replicaId2.dat',replicaId)


    #db = DBSCAN(eps=2.5,min_samples=2).fit(mtx.toarray())
    #core_samples = db.core_sample_indices_
    #labels = db.labels_
    ## Number of clusters in labels, ignoring noise if present.
    #n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #print db
    #print labels
    #print n_clusters_

    #db = DBSCAN(eps=2.8,min_samples=2).fit(mtx.toarray())
    #core_samples = db.core_sample_indices_
    #labels = db.labels_
    ## Number of clusters in labels, ignoring noise if present.
    #n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #print db
    #print labels
    #print n_clusters_

    #####labels_true is the "true" assignment of points to labels: which cluster they should actually belong on. This is available because make_blobs knows which "blob" it generated the point from.

    #print('Estimated number of clusters: %d' % n_clusters_)
    #print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    #print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    #print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    #print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
    #print("Adjusted Mutual Information: %0.3f"% metrics.adjusted_mutual_info_score(labels_true, labels))
    #print("Silhouette Coefficient: %0.3f"% metrics.silhouette_score(X, labels))

