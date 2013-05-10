#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from xml.dom.minidom import parse,parseString
import codecs

XML_FILE="../data/parser/all_clause_parse_utf8.dat"

if __name__ == "__main__":
    with codecs.open(XML_FILE,'r','utf-8') as f:
        SBV_l = []
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
                doc = parseString(xml_string.encode('utf-8'))
                for node in doc.getElementsByTagName("word"):
                    relate = node.getAttribute('relate')
                    pos = node.getAttribute('pos')
                    if relate == "SBV" and pos == "n":
                        SBV_l.append(node.getAttribute('cont').encode('utf-8'))
        SBV_s = set(SBV_l)
        for i in SBV_s:
            print i


