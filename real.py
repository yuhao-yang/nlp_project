# Zixuan Zhang
# 170405
# Using neural network to map 3 features classification probabilities -> class
# input: []
# Usage: python real.py tag_file_path feature_file1_path feature_file2_path feature_file3_path
# here: python real.py tag.txt.test title.txt.prob abstract.txt.prob content.txt.prob

from pybrain.structure import *
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import json
import math
import sys
from pybrain.structure.modules.neuronlayer import NeuronLayer
from pybrain.tools.shortcuts import buildNetwork

'''class StepLayer(NeuronLayer):
    
    def _forwardImplementation(self, inbuf, outbuf):
        outbuf[:] = inbuf**2
    
    def _backwardImplementation(self, outerr, inerr, outbuf, inbuf):
        inerr[:] = 2 * inbuf * outerr

def stepActivationFunction(n):
    if n > 0.5: return 1.
    else: return 0.'''

# create neural network and train it using dataset ds
def formNN(ds):
    '''# create NN: fnn
    fnn = FeedForwardNetwork()

    # 3 layers, input, hidden and output layer
    inLayer = LinearLayer(12, name='inLayer')
    hiddenLayer = SigmoidLayer(7, name='hiddenLayer0')
    outLayer = LinearLayer(4, name='outLayer')

    # add layers to NN
    fnn.addInputModule(inLayer)
    fnn.addModule(hiddenLayer)
    fnn.addOutputModule(outLayer)

    # connect layers
    in_to_hidden = FullConnection(inLayer, hiddenLayer)
    hidden_to_out = FullConnection(hiddenLayer, outLayer)

    # add connection to NN
    fnn.addConnection(in_to_hidden)
    fnn.addConnection(hidden_to_out)

    # make it run
    fnn.sortModules()'''
    
    #fnn = buildNetwork(12, 7, 4, bias=True, hiddenclass=TanhLayer)
    
    fnn = buildNetwork(12, 25, 50, 25, 4, bias=True, hiddenclass=TanhLayer)
    
    print "Training..."
    trainer = BackpropTrainer(fnn, ds, verbose = False, learningrate = 0.01) # , momentum = 0.99
    trainer.trainUntilConvergence(trainingData = ds, validationData = ds, verbose = False, maxEpochs=1000)
    #trainer.trainUntilConvergence(maxEpochs=100000)
    print "finished!"

    return fnn

# get data from tag file and feature files (with probability of tokens)
def getData(tag_file, feature_file1, feature_file2, feature_file3):
    data = []
    i = 0
    j = 0
    
    # tag -> number
    tags = {}
    with open(tag_file, 'r') as f:
        for line in f:
            data.append([])
            tag = str(line.rstrip())
            
            out = [0] * 4
            try:
                out[tags[tag]] = 1
            except KeyError:
                tags[tag] = j
                j += 1
                out[tags[tag]] = 1
            data[i].extend(out)
            i += 1
    f.close()

    i = 0
    with open(feature_file1, 'r') as f1, open(feature_file2, 'r') as f2, open(feature_file3, 'r') as f3:
        line = f1.readline()
        while (line):
            prob1 = json.loads(line.rstrip())
            prob2 = json.loads(f2.readline().rstrip())
            prob3 = json.loads(f3.readline().rstrip())
            
            for tag in tags.keys():
                data[i].append(prob1[tag])
            for tag in tags.keys():
                data[i].append(prob2[tag])
            for tag in tags.keys():
                data[i].append(prob3[tag])
            line = f1.readline()
            i += 1
    f1.close()
    f2.close()
    f3.close()

    return data

# build dataset used in training and testing
def buildDS(data):
    ds = SupervisedDataSet(12, 4)
    
    for ele in data:
        ds.addSample((ele[4], ele[5], ele[6], ele[7], ele[8], ele[9], ele[10], ele[11], ele[12], ele[13], ele[14], ele[15]), (ele[0], ele[1], ele[2], ele[3]))  # 4-15: prob of each feature (in), 0-3: tag info (out)
            
    # split to training and setting
    dsTrain, dsTest = ds.splitWithProportion(0.8)
    return dsTrain, dsTest

if __name__ == '__main__':
    dsTrain, dsTest = buildDS(getData(sys.argv[-4], sys.argv[-3], sys.argv[-2], sys.argv[-1]))
    nn = formNN(dsTrain)
    dsTest = dsTrain

    tot_err = 0
    corr_sum = 0
    for i in range(0, len(dsTest['input'])):
        #for j in range(12):
        #   print dsTest['input'][i][j + 4]
        res = nn.activate((dsTest['input'][i][0], dsTest['input'][i][1], dsTest['input'][i][2], dsTest['input'][i][3], dsTest['input'][i][4], dsTest['input'][i][5], dsTest['input'][i][6], dsTest['input'][i][7], dsTest['input'][i][8], dsTest['input'][i][9], dsTest['input'][i][10], dsTest['input'][i][11]))
        step_res = []
        error = 0
        for j in range(4):
            if res.tolist()[j] > 0.5:
                step_res.append(1)
            else:
                step_res.append(0)
            error += pow(dsTest['target'][i][j] - step_res[-1], 2)
                
        if not error:
            corr_sum += 1
        tot_err += error
        print "Should be: ", dsTest['target'][i].tolist()
        print ", the result is: ", step_res
        print "error: ", error
    print "total error:", tot_err
    print "total_correct:", corr_sum, ", accuracy: ", str(float(corr_sum) / float(len(dsTest['input'])))
