#!/usr/bin/env python2.7
#encoding=utf-8

"""
Setup nlpirpy(a python version of NLPIR2013) to core
"""

from distutils.core import setup, Extension

setup(name="nlpirpy",
  version = '1.0',
  description = 'python version for NLPIR',
        py_modules=['nlpirpy'],
        ext_modules=[Extension('_nlpirpy',
            language='c++',
            libraries = ['NLPIR','_nlpirpy'],
            )]
     )


