
"""
"""

from FileIO import FileIO 
FEATURE_PATH = "../data/features/"

if __name__ == "__main__":
    fio = FileIO()
    rid_url = fio.readFileToDict(FEATURE_PATH+"url_id_feature.dat")
    rid_sent = fio.readFileToDict(FEATURE_PATH+"rid_sentratio.dict")
    rid_general = fio.readFileToDict(FEATURE_PATH+"rid_general.dict")
    rid_len = fio.readFileToDict(FEATURE_PATH+"rid_lenratio.dict")
    rid_cate = fio.readFileToDict(FEATURE_PATH+"rid_cateratio.dict")
    #rid_detailed = fio.readFileToDict()
    
    rid_objective = {}
    count = 0

    for rid in rid_url.keys():
        #print rid_url[rid]
        #print rid_sent[rid]
        #print rid_general[rid]
        #print rid_len[rid]
        #print rid_cate[rid]
        #rid_objective[rid] = sum([float(rid_url[rid]),float(rid_sent[rid]),float(rid_general[rid]),float(rid_len[rid]),float(rid_cate[rid])])
        rid_objective[rid] = 0.25*float(rid_url[rid])+0.1*float(rid_sent[rid])+0.3*float(rid_general[rid])+0.15*float(rid_len[rid])+0.2*float(rid_cate[rid])

    #threshold = 5
    #print len([v for v in rid_objective.values() if v > 1])

    rid_objective = sorted(rid_objective.items(), key= lambda x:x[1],reverse = True)

    for k,v in rid_objective:
        print "%s\t\t%f"%(k,v)
    #fio.recordToFile(FEATURE_PATH+"rid_objective.dict",rid_objective)




