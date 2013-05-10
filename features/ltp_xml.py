#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from xml.dom.minidom import parse,parseString

class ltpXML:
    def __init__(self,sentence,xml_str):
        self.sentence = sentence
        self.xml_str = xml_str
        self.relate_list = self.get_relate_list()
        self.word_list = self.get_word_list()

    def get_clause_relate_path(self):
        relate_str = ""
        for i in self.relate_list:
            relate_str += (i+"@")
        return relate_str.rstrip('@')
        
    def get_word_list(self):
        doc = parseString(self.xml_str)
        return [node.getAttribute('cont') for node in doc.getElementsByTagName('word')]
    
    
    def get_relate_list(self):
        doc = parseString(self.xml_str)
        return [node.getAttribute('relate') for node in doc.getElementsByTagName("word")]



