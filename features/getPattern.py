#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
from xml.dom.minidom import parse,parseString
import codecs
from FileIO import FileIO

XML_FILE="../data/parser/all_clause_parse_utf8.dat"
FINDING_PATTERN = ["ADV@HED","SBV@ADV@HED","SBV@ADV@ADV@HED","ADV@ADV@HED","ADV@HED@MT","ATT@SBV@ADV@HED","SBV@ADV@HED@MT","ADV@HED@VOB","ADV@DE@ATT@HED","SBV@ADV@HED@VOB","CNJ@ADV@HED","ADV@DE@HED","SBV@ADV@DE@HED","DE@ATT@SBV@ADV@HED","ADV@HED@ATT@VOB","DE@ATT@ADV@HED"]
FINDING_RELATE = "ADV"
WORD_FILE = "data/pattern/ADV.dat"

if __name__ == "__main__":
    fio = FileIO()
    highfreq_clauses = fio.readFileToList("data/high_freq_clauses.dat")
    relate_clauselist = {}
    word_list = []#specific word with specific relation,record them to file for more use
    with codecs.open(XML_FILE,'r','utf-8') as f:
        #print "Read file and store relateString and clause into memory..."
        count = 0
        while(True):
            line = f.readline()
            if not line:
                break
            if line.startswith('Input'):
                clause = line.strip('\n').split(': ',2)[1]
                f.readline()
                xml_string = ""
                xml_line = ""
                while(not xml_line.startswith("</xml4nlp>")):
                    xml_line = f.readline()
                    xml_string+=xml_line
                if not clause.encode('utf-8') in highfreq_clauses:
                    continue
                doc = parseString(xml_string.encode('utf-8'))
                relates = [node.getAttribute('relate') for node in doc.getElementsByTagName("word")]
                words = [node.getAttribute('cont') for node in doc.getElementsByTagName("word")]
                relateString = ""
                for i in relates:
                    relateString+=(i+"@")
                relateString = relateString.rstrip('@')
                if relateString in FINDING_PATTERN:
                    word_list.append(words[relates.index(FINDING_RELATE)].encode('utf-8'))
                if not relate_clauselist.has_key(relateString):
                    relate_clauselist[relateString] = []
                relate_clauselist[relateString].append(clause)

    #print len(relate_clauselist),"relations"

    #sort relate_clauses by number of clauses
    sorted_relate_clauses = sorted(relate_clauselist.items(),key = lambda x:len(x[1]),reverse = True)
    for k,clausel in sorted_relate_clauses:
        print k
        for i in clausel:
            print i.encode('utf-8')

    fio.recordToFile(WORD_FILE,set(word_list))
