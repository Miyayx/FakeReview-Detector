#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import re
import sys
sys.path.append('/home/yang/GraduationProject/')
 
from utils import fileio
from utils.cutclause import SentenceCutter

regulars = [
    re.compile(ur"[\u4e00-\u9fa5]想象中"),
    re.compile(ur"没[\u4e00-\u9fa5]?(?:想象中|图片上|图片中)"),
    re.compile(ur"[没有|超乎|没]想[象|像][的|得][\u4e00-\u9fa5]+"),
    re.compile(ur"(?:比|跟|没有)+(?:想象中|图片上|图上|照片上)+的(?:一模一样|一样|好|差不多|好看)"),
    re.compile(ur"[\u4e00-\u9fa5]*[跟和与](?:照片|图片|描述|实物|店家描述|卖家描述)+的?(?:上的|中的)?(完全)?[(一样)|(一致)|(没有差距)]"),
    re.compile(ur"(?:几乎|也|基本)?[\u4e00-\u9fa5]*没有?色差"),
    re.compile(ur"我买的是?[\u4e00-\u9fa5]+$"),
    re.compile(ur"第[\u4e00-\u9fa5|0-9]次[\u4e00-\u9fa5](?:买|来|光顾)"),
    re.compile(ur"第[\u4e00-\u9fa5|0-9]次[在|来]?[\u4e00-\u9fa5]{2,4}买(?:包|包包|东西)+"),
    re.compile(ur"已经买了[\u4e00-\u9fa5|0-9]个"),
    re.compile(ur"(?:下次|以后)*(肯定)?还?会[再在]?[来次]?(?:光顾|光临)?的?"),
    re.compile(ur"[\u4e00-\u9fa5]*一[分|份]价{0,1}钱一[分|份]货"),
    re.compile(ur"以后买包就[\u4e00-\u9fa5]*家了"),
    re.compile(ur"以后就[\u4e00-\u9fa5]*家买[\u4e00-\u9fa5]*了"),
    re.compile(ur"祝[\u4e00-\u9fa5]*生意兴隆[\u4e00-\u9fa5]?"),
    re.compile(ur"[\u4e00-\u9fa5]*还是一如既往[地|的]"),
    re.compile(ur"(已经)?是?第[\u4e00-\u9fa5|0-9]次[\u4e00-\u9fa5]*(?:买|购买|光顾|来)了?"),
    re.compile(ur"(已经)?是?老(?:顾客|客户)了?"),
    re.compile(ur"[\u4e00-\u9fa5]*很[\u4e00-\u9fa5]*很(?:喜欢|不错)"),
    re.compile(ur"[\u4e00-\u9fa5]*很(?:喜欢|满意)"),
    re.compile(ur"好评[\u4e00-\u9fa5|0-9]分"),
    re.compile(ur"[\u4e00-\u9fa5]*也?[挺超]?给力[\u4e00-\u9fa5]"),
    re.compile(ur"这个价[格钱]?买到这样的包"),
    re.compile(ur"这个价[格钱]?(?:很|非常|太)值"),
    re.compile(ur"[\u4e00-\u9fa5]*这个价[格钱]?也?[\u4e00-\u9fa5]{1,3}了"),
    #re.compile(ur"包{1,2}[\u4e00-\u9fa5]{2,3}的$"),
    re.compile(ur"[\u4e00-\u9fa5]*是?[帮给][\u4e00-\u9fa5]*[买带拍]的"),
    re.compile(ur"买来?[送|给][\u4e00-\u9fa5]*的?"),
    re.compile(ur"[\u4e00-\u9fa5]*不影响(?:整体|使用|美观)+"),
    re.compile(ur"[与跟和](?:卖家|买家|老板|店主)+描述[的得](基本)?(?:一致|一样)"),
    re.compile(ur"就是[\u4e00-\u9fa5]*不[太大]好"),
    re.compile(ur"(?:就是|只是|不过)[\u4e00-\u9fa5]+有点?[\u4e00-\u9fa5]*"),
    re.compile(ur"[给全][\u4e00-\u9fa5|0-9]{1,2}分(好评)?"),
    re.compile(ur"[\u4e00-\u9fa5]{1,3}都说挺好的"),
    re.compile(ur"真的很[\u4e00-\u9fa5]*哦"),
    re.compile(ur"[\u4e00-\u9fa5]{1,3}看了[\u4e00-\u9fa5]{0,3}很喜欢"),
    re.compile(ur"[\u4e00-\u9fa5]{1,3}说质量不错"),
    re.compile(ur"就是[\u4e00-\u9fa5]*不给力"),
    re.compile(ur"和[\u4e00-\u9fa5]*一人[\u4e00-\u9fa5]*一个"),
    re.compile(ur"[\u4e00-\u9fa5]*和[\u4e00-\u9fa5]*都挺[\u4e00-\u9fa5]*的"),
    re.compile(ur"一直很喜欢[\u4e00-\u9fa5]*的包"),
    re.compile(ur"(?:总体|整体|总得|总之)(来说)?(?:挺|很|还|比较)?(?:可以|不错|满意|喜欢|好)"),
    re.compile(ur"[\u4e00-\u9fa5]*的一次[\u4e00-\u9fa5]*[网购|购物]+"),
    re.compile(ur"[\u4e00-\u9fa5]*(?:网购|购物)+[\u4e00-\u9fa5]*最[\u4e00-\u9fa5]+的一次"),
    re.compile(ur"第一次[\u4e00-\u9fa5]{1,3}$"),
    re.compile(ur"[\u4e00-\u9fa5]{1,4}买了[\u4e00-\u9fa5]{1,3}个包{0,2}"),
    re.compile(ur"这家比其他的返利网要返的[\u4e00-\u9fa5]*很多"),
    re.compile(ur"双[\u4e00-\u9fa5]*买的"),
    re.compile(ur"[\u4e00-\u9fa5]*也?是我(?:喜欢|想象|想像|想要)+的[\u4e00-\u9fa5]*"),
    re.compile(ur"[很|非常][\u4e00-\u9fa5]*的一款包"),
    re.compile(ur"[\u4e00-\u9fa5]*可以[\u4e00-\u9fa5]*很多东西"),
    re.compile(ur"[\u4e00-\u9fa5]+就(?:好|行|可以|没事|可以)了$"),
    re.compile(ur"[\u4e00-\u9fa5]*一如既往[的得]好"),
    re.compile(ur"性价比很[\u4e00-\u9fa5]*的一款包{1,2}"),
    re.compile(ur"[买背用]了[\u4e00-\u9fa5]{1,2}[天个只次]了?$"),
    re.compile(ur"[\u4e00-\u9fa5]*(?:谢谢|感谢)[\u4e00-\u9fa5]*的小礼物"),
    re.compile(ur"[\u4e00-\u9fa5]*[谢谢|感谢][\u4e00-\u9fa5]*送的[\u4e00-\u9fa5]*"),
    re.compile(ur"跟大家(?:分析|分享)一下"),
    re.compile(ur"(?:同事|同学|朋友)+们?[都也]+说?[很挺]?(?:好看|不错|好|喜欢)+"),
    re.compile(ur"(?:同事|同学|朋友)+们?[\u4e00-\u9fa5]*[都也]想买"),
    re.compile(ur"[\u4e00-\u9fa5]*很百搭"),
    re.compile(ur"[不过|但是]?[\u4e00-\u9fa5]*真的很好"),
    re.compile(ur"[\u4e00-\u9fa5]*[看摸背](?:起来|着|上去)也?很?还?[\u4e00-\u9fa5]*"),
    re.compile(ur"(?:店家|买家|卖家|老板)的?(服务)?态度也?很?[\u4e00-\u9fa5]*"),
    re.compile(ur"(真是)?(?:物美价廉|价廉物美|物有所值|物超所值|爱不释手)[\u4e00-\u9fa5]*"),
    re.compile(ur"值得(?:购买|推荐|入手|买)+[\u4e00-\u9fa5]?$"),
    re.compile(ur"包{0,2}送[\u4e00-\u9fa5]+的$"),
    re.compile(ur"[\u4e00-\u9fa5]+了点$"),
    re.compile(ur"[\u4e00-\u9fa5]+没得说$"),
    re.compile(ur"又[\u4e00-\u9fa5]+又[\u4e00-\u9fa5]+$"),
    re.compile(ur"[\u4e00-\u9fa5]+收到[\u4e00-\u9fa5]$"),
    re.compile(ur"虽然不是[\u4e00-\u9fa5]+皮的$"),
    re.compile(ur"就是味道?[\u4e00-\u9fa5]+了[\u4e00-\u9fa5]?点?"),
    re.compile(ur"[\u4e00-\u9fa5]*没有(?:异味|味道)"),
    re.compile(ur"[\u4e00-\u9fa5]+天下午[\u4e00-\u9fa5]的"),
    re.compile(ur"跟[\u4e00-\u9fa5]+一起买的"),
    re.compile(ur"(?:卖家|店家|老板)发货速度[\u4e00-\u9fa5]+"),
    re.compile(ur"[\u4e00-\u9fa5]+(?:也|都是|是)我喜欢的"),
    re.compile(ur"买的[\u4e00-\u9fa5]+色的"),
    re.compile(ur"第?[\u4e00-\u9fa5|0-9]天就收?到了"),
    re.compile(ur"(不好意思)?[\u4e00-\u9fa5]+晚了"),
    re.compile(ur"没有?让?[\u4e00-\u9fa5]*失望"),
    re.compile(ur"[\u4e00-\u9fa5]+有点小[\u4e00-\u9fa5]+"),
    re.compile(ur"[\u4e00-\u9fa5]+还是给个好评"),
    re.compile(ur"和[\u4e00-\u9fa5]+一样好"),
    #re.compile(ur"[\u4e00-\u9fa5]+超好"),
    re.compile(ur"适合[\u4e00-\u9fa5]天"),
    re.compile(ur"走了[\u4e00-\u9fa5|0-9]{1,3}天"),
    re.compile(ur"[\u4e00-\u9fa5]{1,3}很羡慕"),
    re.compile(ur"[\u4e00-\u9fa5]*比[\u4e00-\u9fa5]*便宜"),
    re.compile(ur"(?:多|继续)捧场"),
    re.compile(ur"很(?:划算|换算)"),
    re.compile(ur"不要犹豫"),
    re.compile(ur"大爱"),
    re.compile(ur"[\u4e00-\u9fa5]{1,3}超值"),
    re.compile(ur"完全超出期望"),
    re.compile(ur"考虑[\u4e00-\u9fa5]{0,2}周到"),
    re.compile(ur"哈哈"),
    re.compile(ur"复古[\u4e00-\u9fa5]+"),
    re.compile(ur"[\u4e00-\u9fa5]{2,3}(看了)?也很?喜欢"),
    re.compile(ur"非常满意")
    ]

def general_value(reviews):
    pass

def general_proc(reviewobj):
    general_count = 0
    for c in reviewobj["clauses"]:
        for regular in regulars:
            if re.match(regular,c):
                general_count+=1
                break
    reviewobj["general"] = general_count
    return float(general_count)/len(reviewobj["clauses"]) if len(reviewobj["clauses"]) > 0 else 0
    
if __name__=="__main__":

    #reviewList = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
    #rid_generalratio = {}
    #for rid,review in reviewList:
    #    sc = SentenceCutter(review)
    #    clauses = sc.cutToClauses()
    #    general_count = 0
    #    for c in clauses:
    #        for regular in regulars:
    #            if re.match(regular,c):
    #                general_count+=1
    #                break
    #    ratio = float(general_count)/len(clauses)
    #    print "%s\t\t%f"%(rid,ratio)

    review = "颜色很正！！！包包超值了！！！做工精致，皮质柔软舒服，没有异味，挂牌正规！！！总之是太欢喜啦！！！"
    sc = SentenceCutter(review)
    clauses = sc.cutToClauses()
    for c in clauses:
        for regular in regulars:
            if re.match(regular,c):
                print c
                break
  

