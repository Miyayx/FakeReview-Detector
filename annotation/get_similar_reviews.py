#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import shingling
import sys
sys.path.append("/home/yang/GraduationProject/utils/")
import fileio

if __name__ == "__main__":
     reviewList = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
     id_review = dict(reviewList)

     id_list = fileio.read_file_to_list("../data/target/shingle_id1.dat")
     
     id_seq = dict([eval(rid),shingling.ngram_sequence(4,r)] for rid,r in id_review.iteritems() if eval(rid) in id_list)        
     similar_ids = []

     for i in range(len(id_list)):
         id1 = id_list[i]
         r1 = id_review[str(id1)]
         if len((r1.decode('utf-8'))) < 12:
             continue
         seq1 = id_seq[id1]
         for j in range(i+1,len(id_list)):
             id2 = id_list[j]
             r2 = id_review[str(id2)]
             seq2 = id_seq[id2]
             similar = shingling.jaccard_seq(seq1,seq2)
             if similar > 0.4:
                 similar_ids.append(id1)
                 similar_ids.append(id2)
                 print id1
                 print r1
                 print id2
                 print r2
                 print similar
                 print "============================="
     similar_ids = set(similar_ids)
     #fileio.record_to_file("../data/target/shingle_id2.dat",similar_ids)

