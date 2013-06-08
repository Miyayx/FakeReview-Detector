#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from ReviewCrawler.DictUnicodeWriter import DictUnicodeWriter
from utils import fileio
def id_to_csv(filename):
    fieldnames = ['id','reviewContent', 'reviewTime', 'degree','userNick', 'userId','userLink','appendId','appendReview','appendTime']
    id_list = fileio.read_file_to_list(filename)
    review_list = fileio.read_fields_from_allcsv("data/CSV/Train/",fieldnames)

    dataL = []
    for item in review_list:
        if eval(item[0]) in id_list[:100]:
            data = {}
            for i in range(len(fieldnames)):
                data[fieldnames[i]] = item[i]
            dataL.append(data)
    
    fname = "test.csv"
    with open(fname,'w') as f:
        dict_writer = DictUnicodeWriter(f,fieldnames,delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(dataL)

if __name__=="__main__":
    id_to_csv("data/target/replica_high_freq_all.dat")
