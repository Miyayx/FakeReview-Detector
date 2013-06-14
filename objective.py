
"""
"""

from utils import fileio 
import math

FEATURE_PATH = "data/features/"

def objective(reviewobj):
    w = [0.3,0.15,0.1,0.2,0.25]
    features = [float(reviewobj["url"]),float(reviewobj["sentiment"]),float(reviewobj["general"]),float(reviewobj["general"]),float(reviewobj["length"]),1]
    result = 0
    for i in range(len(w)):
        result+=w[i]*features[i]

    threshold = 0.3 
    print "objective",result
    return True if result > threshold else False

def logistic_objective(reviewobj):
    #w = [6,4.5,3.5,6,8,-7]
    w = [10,4.5,3.5,6.8,9,-6.5]
    features = [float(reviewobj["url"]),float(reviewobj["sentiment"]),float(reviewobj["general"]),float(reviewobj["general"]),float(reviewobj["length"]),1]
    score = 0
    for i in range(len(w)):
        score+=w[i]*features[i]
    result = 1/(1+math.exp(score))

    threshold = 0.5
    print "lr_objective",result
    return True if result < threshold else False

if __name__ == "__main__":

    review_list = fileio.read_fields_from_allcsv("data/CSV/Train/",["id","reviewContent"])
    rid_review = dict(review_list)

    #rid_url = fileio.read_file_to_dict(FEATURE_PATH+"url_id_feature.dat")
    rid_url = fileio.read_file_to_dict(FEATURE_PATH+"rid_url.dict")
    rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentnorm.dict")
    #rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentratio.dict")
    rid_general = fileio.read_file_to_dict(FEATURE_PATH+"rid_general.dict")
    rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenrationorm.dict")
    #rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lennorm.dict")
    #rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenratio.dict")
    #rid_cate = fileio.read_file_to_dict(FEATURE_PATH+"rid_cateratio.dict",delimiter=None)
    rid_cate = fileio.read_file_to_dict(FEATURE_PATH+"rid_catenorm.dict")

    detect_list = fileio.read_file_to_list("data/target/all_fake.dat")
    suspicion_list = fileio.read_file_to_list("data/target/suspicion_id.dat")
    suspicion_list = suspicion_list+detect_list
    rid_objective = {}
    count = 0
    
    #for rid in detect_list:
    for rid in rid_url.keys():
        #rid_objective[rid] = sum([float(rid_url[rid]),float(rid_sent[rid]),float(rid_general[rid]),float(rid_len[rid]),float(rid_cate[rid])])
        try:
            rid_objective[rid] = \
            0.25*float(rid_url[rid])+\
            0.2*float(rid_sent[rid])+\
            0.2*float(rid_general[rid])+\
            0.15*float(rid_len[rid])+\
            0.2*float(rid_cate[rid])
        except:
            print rid

    rid_objective = sorted(rid_objective.items(), key= lambda x:x[1],reverse = True)

    fake_count = 0
    for rid,v in rid_objective:
        if len(rid_review[str(rid)].decode('utf-8')) > 10 and v > 0.2 and (not rid in suspicion_list):
            fake_count+=1
            print rid
        #print "*************************************"
        #print "rid",rid
        #print rid_review[str(rid)]
        #print "url",rid_url[rid]
        #print "sent",rid_sent[rid]
        #print "general",rid_general[rid]
        #print "len",rid_len[rid]
        #print "category",rid_cate[rid]
        #print "objective",v
    #print fake_count

    #for k,v in rid_objective:
    #    print "%s\t\t%f"%(k,v)

