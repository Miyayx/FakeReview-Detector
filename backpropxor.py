#!/usr/bin/env python
# A simple feedforward neural network that learns XOR.

from xor_data import XORDataSet #@UnresolvedImport
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer

def testTraining():
    print "Reading data"
    d = XORDataSet()
    traind,testd = d.splitWithProportion(0.8)
    print "Building network"
    n = buildNetwork(traind.indim, 4, traind.outdim, recurrent=True)
    print "Training"
    t = BackpropTrainer(n, learningrate = 0.01, momentum = 0.99, verbose = True)
    t.trainOnDataset(traind,100)
    testd = XORDataSet(begin=60000,end=80000)
    print t.module.params
    t.testOnData(testd,verbose= True)


if __name__ == '__main__':
    testTraining()
