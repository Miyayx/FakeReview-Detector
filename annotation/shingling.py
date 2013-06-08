#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

def ngram_sequence(n,string):
    string = list(string)
    sequence = []
    for i in range(len(string)-4):
        s = string[i]+string[i+1]+string[i+2]+string[i+3]
        sequence.append(s)
    return list(set(sequence))

def jaccard_str(s1,s2):
    seq1 = ngram_sequence(4,s1)
    seq2 = ngram_sequence(4,s2)
    return jaccard_seq(seq1,seq2)

def jaccard_seq(seq1,seq2):
    same = [s for s in seq1 if s in seq2]
    total = set(seq1+seq2)
    return float(len(same))/len(total)


if __name__ == "__main__":
    s1 = u"非常好，性价比非常高的一个包包，黑色很显档次，旅游休闲购物一个包就搞定，肩带很稳固，柳钉很结实，很好，背了好几天了，全五分！"
    s2 = u"非常好，性价比非常高的一个包包，黑色很显档次，旅游休闲购物一个包就搞定，肩带很稳固，柳钉很结实，很好，背了好几天了，说28包邮同事们都不相信呢，以后会再来帮衬，全五分！"
    ss1 = "包包挺好的，姐姐很喜欢，物流很给力，包包和图片上的一样，\(^o^)/~"
    ss2 = "很好很漂亮，包包挺好的，姐朋友很喜欢，物流很给力，包包和图片上的一样，5分"
    print jaccard(ss1,ss2)




