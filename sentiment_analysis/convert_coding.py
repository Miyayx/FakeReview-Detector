#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import codecs
import os
import shutil
import chardet

def convert_encoding(filename, target_encoding):
    # Backup the origin file.
    shutil.copyfile(filename, filename + '.bak')
    # convert file from the source encoding to target encoding
    content = codecs.open(filename, 'r').read()
    source_encoding = chardet.detect(content)['encoding']
    print source_encoding, filename
    content = content.decode(source_encoding) #.encode(source_encoding)
    codecs.open(filename, 'w', encoding=target_encoding).write(content)


