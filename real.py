# Zixuan Zhang
# 170405
# Using neural network to map 3 features classification probabilities -> class
# input: []

from pybrain.structure import *
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import json
import sys

def formNN(ds):

    # form nn
    # create NN: fnn
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
    fnn.sortModules()
    
    print "Training..."
    trainer = BackpropTrainer(fnn, ds, verbose = False, learningrate=0.01)
    #trainer.trainUntilConvergence(trainingData = DS, validationData = DS)
    trainer.trainUntilConvergence()
    print "finished!"

    return fnn

def getData(tag_file, feature_file1, feature_file2, feature_file3):
    data = []
    with open(tag_file, 'r') as f:
        
        prior_probabilities = json.loads(f.readline().rstrip())
        probabilities = json.loads(f.readline().rstrip())
    f.close()

def dsBuild(data):
    # form data
    DS = SupervisedDataSet(12, 4)
    
    for ele in data:
        ds.addSample((ele[4], ele[5], ele[6], ele[7], ele[8], ele[9], ele[10], ele[11], ele[12], ele[13], ele[14], ele[15]), (ele[0], ele[1], ele[2], ele[3]))
    dsTrain, dsTest = ds.splitWithProportion(0.8)
    return dsTrain, dsTest

if __name__ == '__main__':
    dsTrain, dsTest = dsBuild(getData(sys.argv[-4], sys.argv[-3], sys.argv[-2], sys.argv[-1]))
    nn = formNN(dsTrain)
    dsTest = dsTrain

    for i in range(0, len(dsTest['input'])):
        res = nn.activate((dsTest['input'][i][4], dsTest['input'][i][5], dsTest['input'][i][6], dsTest['input'][i][7], dsTest['input'][i][8], dsTest['input'][i][9], dsTest['input'][i][10], dsTest['input'][i][11], dsTest['input'][i][12], dsTest['input'][i][13], dsTest['input'][i][14], dsTest['input'][i][15]))
        error = dsTest['target'][i][0] + dsTest['target'][i][1] + dsTest['target'][i][2] + dsTest['target'][3][0] - res[0] - res[1] - res[2] - res[3]
        print error
