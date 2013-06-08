#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
sys.path.append("/home/yang/GraduationProject/utils/")
import fileio

def remove_zero(t):
    return tuple(k for k in t if k!=0)

if __name__ == "__main__":
    temps = fileio.read_file_to_list("cluster_temp2.dict")
    temp_rid = fileio.read_file_to_dict("data/temp_and_rid.dat")
    new_temp_rid = dict()
    for k,v in temp_rid.items():
        nk = remove_zero(k)
        if new_temp_rid.has_key(nk):
            new_temp_rid[nk].extend(v)
        else:new_temp_rid[nk] = v

    rid_list = []

    for temp in temps:
        t = temp.split(None,1)[1]
        t = t.rsplit(None,1)[0]
        #print t
        t = eval(t)
        t = remove_zero(t)
        #if not t in temp_rid.keys():
        #    try:
        #        print t
        #        t = list(t)
        #        t.reverse()
        #        t.remove(0)
        #        t.reverse()
        #        t = tuple(t)
        #        print t
        #        rid_list.extend(temp_rid[t])
        #    except:
        #        print t
        #        t = list(t)
        #        t.remove(0)
        #        t = tuple(t)
        #        print t
        #        rid_list.extend(temp_rid[t])
        #    else:
        try:
            rid_list.extend(new_temp_rid[t])
        except:
            #print t
            for k in new_temp_rid.keys():
                if len(k) == len(t)+1:
                    newk = list(k)
                    newt = list(t)
                    if len(set(newk+newt)) == len(newk) and newk[0] == newt[0]:
                        #print k
                        #print t
                        rid_list.extend(new_temp_rid[k])

    
    for rid in rid_list:
        print rid


