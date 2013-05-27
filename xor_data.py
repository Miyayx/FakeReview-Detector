#!/usr/bin/env python
import random

from features import fileio 
from pybrain.datasets import SupervisedDataSet

FEATURE_PATH = "data/features/"

class XORDataSet(SupervisedDataSet):
    """ A dataset for the XOR function."""
    def __init__(self,begin=0,end=40000):
        SupervisedDataSet.__init__(self, 5, 1)

        rid_url = fileio.read_file_to_dict(FEATURE_PATH+"url_id_feature.dat")
        rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentratio.dict")
        rid_general = fileio.read_file_to_dict(FEATURE_PATH+"rid_general.dict")
        rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenratio.dict")
        rid_cate = fileio.read_file_to_dict(FEATURE_PATH+"rid_cateratio.dict",delimiter=None)
        
        fake = fileio.read_file_to_list("data/target/all_replicaId.dat")

        for rid in rid_url.keys()[begin:end]:
            inps = [rid_url[rid],rid_sent[rid],rid_general[rid],rid_len[rid],rid_cate[rid]]
            target = [1 if rid in fake else 0]
            self.addSample(inps,target)

