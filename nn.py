# Zixuan Zhang
# 170405
# Using neural network to map 3 features classification probabilities -> class
# input: 3 feature file + 1 tag file (same row = same novel)
# ouput: test set result & accuracy from input (0.2)
# Usage: python nn.py all_tag_file_path tag_file_path feature_file1_path feature_file2_path feature_file3_path
# here: python nn.py data/tag4.txt.list data/tag4.txt.test data/title4.txt.prob data/abs4.txt.prob data/content4.txt.prob

from pybrain.structure import *
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import json
import math
import sys
from pybrain.structure.modules.neuronlayer import NeuronLayer
from pybrain.tools.shortcuts import buildNetwork
import io

'''class StepLayer(NeuronLayer):
    
    def _forwardImplementation(self, inbuf, outbuf):
    outbuf[:] = inbuf**2
    
    def _backwardImplementation(self, outerr, inerr, outbuf, inbuf):
    inerr[:] = 2 * inbuf * outerr
    
    def stepActivationFunction(n):
    if n > 0.5: return 1.
    else: return 0.'''

# create neural network and train it using dataset ds
def formNN(tag_num, ds):
    # create NN: fnn
    fnn = FeedForwardNetwork()
    
    # 3 layers, input, hidden and output layer
    inLayer = LinearLayer(tag_num * 3, name='inLayer')
    hiddenLayer = SigmoidLayer(7, name='hiddenLayer0')
    outLayer = LinearLayer(tag_num, name='outLayer')
    
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
    
    #fnn = buildNetwork(tag_num * 3, 7, tag_num, bias=True, hiddenclass=TanhLayer)
    
    #fnn = buildNetwork(tag_num * 3, 25, 50, 25, tag_num, bias=True, hiddenclass=TanhLayer)
    
    print "Training..."
    trainer = BackpropTrainer(fnn, ds, verbose = False, learningrate = 0.01) # , momentum = 0.99
    #trainer.trainUntilConvergence(trainingData = ds, validationData = ds, verbose = True, maxEpochs=1000)
    for epoch in range(0, 1000):
        error = trainer.train()
        if error < 0.001:
            break
    #trainer.trainUntilConvergence(maxEpochs=100000)
    print "finished!"
    
    return fnn

# get data from tag file and feature files (with probability of tokens) in vector[class belonging..., tag probabilities...]
# class belonging: ith class: only ith element is 1, else 0
# tag probabilities: in particular fixed order (key of map)
def getData(all_tag, tag_file, feature_file1, feature_file2, feature_file3):
    data = []
    
    # get number of tags from all_tag_file
    print "Getting all tags/classes..."
    tag_num = 0
    with io.open(all_tag, mode = 'r', encoding = 'utf-8') as f:
        tag_num = len(json.loads(f.readline().rstrip()))

    # add tag info([0, 1, 0, 0...]) to data matrix
    # can be moved in all_tag section
    print "Getting tag info for each records..."
    tags = {} # {tag1: 1; tag2: 2}, tag and its position (in appearing order)
    #tag_goto_num = {}
    with io.open(tag_file, mode = 'r', encoding = 'utf-8') as f:
        i = 0
        j = 0
        # add a tuple per line
        for line in f:
            data.append([])
            tag = line.rstrip()
            out = [0] * tag_num
            try:
                out[tags[tag]] = 1  # only the position of the tag is given 1, others is still 0
            #tag_goto_num[tag] += 1
            except KeyError:    # no such key(tag): add to map and give it a position number in increasing order
                tags[tag] = j
                j += 1
                out[tags[tag]] = 1
            #tag_goto_num[tag] = 0
            data[i].extend(out)
            i += 1
    #print tag_goto_num

# get tag probability of each feature and add to data matrix
print "Getting tag probabilities from each feature..."
    with io.open(feature_file1, mode = 'r', encoding = 'utf-8') as f1, io.open(feature_file2, mode = 'r', encoding = 'utf-8') as f2, io.open(feature_file3, mode = 'r', encoding = 'utf-8') as f3:
        line = f1.readline()
        i = 0
        while (line):
            prob1 = json.loads(line.rstrip())
            prob2 = json.loads(f2.readline().rstrip())
            prob3 = json.loads(f3.readline().rstrip())
            
            for tag in tags.keys():
                # the order doesn't matter as long as it is the same for every record: all same neutron
                data[i].append(prob1[tag])
                data[i].append(prob2[tag])
                data[i].append(prob3[tag])
            
            line = f1.readline()
            i += 1

return tag_num, data

# normalize tag probabilities
def norm(tag_num, data):
    print "Normalizing..."
    end = len(data[0])
    data_length = len(data)
    for i in range(tag_num, end):   # row
        # get max, min and range
        '''max = data[0][i]
            min = data[0][i]
            for j in range(data_length):    # column
            if data[j][i] > max:
            max = data[j][i]
            elif data[j][i] < min:
            min = data[j][i]
            ran = max - min
            
            # normalize to 0 ~ 1
            for j in range(data_length):
            data[j][i] = (data[j][i] - min) / ran'''
        
        sum = 0
        std = 0
        # get sum (to calculate mean)
        for j in range(data_length):
            sum += data[j][i];
        mean = sum / float(data_length)
        
        # get standard deviation
        for j in range(data_length):
            std += pow(data[j][i] - mean, 2);

#!! only to training set!: normalize test set using mean and std of training set
# normalization
for j in range(data_length):
    data[j][i] = (data[j][i] - mean) / std;
    
    return data



# build dataset used in training and testing
def buildDS(tag_num, data):
    print "Building data set..."
    # feature: 3
    ds = SupervisedDataSet(tag_num * 3, tag_num)
    
    for ele in data:
        #ds.addSample((ele[4], ele[5], ele[6], ele[7], ele[8], ele[9], ele[10], ele[11], ele[12], ele[13], ele[14], ele[15]), (ele[0], ele[1], ele[2], ele[3]))  # 4-tag_num * 3: prob of each feature (in), 0-3: tag info (out)
        ds.addSample(ele[tag_num:], ele[:tag_num])
    
    # split to training and setting
    dsTrain, dsTest = ds.splitWithProportion(0.8)
    return dsTrain, dsTest

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "not enogh parameter! input: "
        print "python real.py all_tag_file_path tag_file_path feature_file1_path feature_file2_path feature_file3_path"
        sys.exit()
    '''try:
        all_tag_file_path, tag_file_path, feature_file1_path, feature_file2_path, feature_file3_path = sys.argv[-5], sys.argv[-4], sys.argv[-3], sys.argv[-2], sys.argv[-1]
        except IndexError:
        print "parameter error! input format: "
        print "python real.py all_tag_file_path tag_file_path feature_file1_path feature_file2_path feature_file3_path"
        sys.exit()'''
    tag_num, data = getData(sys.argv[-5], sys.argv[-4], sys.argv[-3], sys.argv[-2], sys.argv[-1])
    data = norm(tag_num, data)
    dsTrain, dsTest = buildDS(tag_num, data)
    
    print dsTest['input']
    
    nn = formNN(tag_num, dsTrain)
    #dsTest = dsTrain
    
    tot_err = 0
    corr_sum = 0
    #!! why the results are the same?! no normalization, data bias
    for i in range(0, len(dsTest['input'])):
        #print 'deTest[\'input\'][\'i\']:', dsTest['input'][i]
        #for j in range(12):
        #   print dsTest['input'][i][j + 4]
        res = nn.activate(dsTest['input'][i])
        #res = nn.activate((dsTest['input'][i][0], dsTest['input'][i][1], dsTest['input'][i][2], dsTest['input'][i][3], dsTest['input'][i][4], dsTest['input'][i][5], dsTest['input'][i][6], dsTest['input'][i][7], dsTest['input'][i][8], dsTest['input'][i][9], dsTest['input'][i][10], dsTest['input'][i][11]))
        #step_res = []
        list_res = res.tolist()
        list_tar = dsTest['target'][i].tolist()
        #print list_res
        step_res = [0] * tag_num
        error = 0
        max = 0
        max_posi = 0
        for j in range(tag_num):
            '''if res.tolist()[j] > 0.5:
                step_res.append(1)
                else:
                step_res.append(0)'''
            '''step_res.append(res.tolist()[j])'''
            if list_res[j] > max:
                #print 'list_res[j] =', list_res[j], 'max =', max, 'this_posi =', j
                max = list_res[j]
                max_posi = j
        #error += pow(dsTest['target'][i][j] - step_res[-1], 2)
        step_res[max_posi] = 1
        if list_tar[max_posi] != 1:
            error = 2
            #if error:
            tot_err += error
                else:
                    corr_sum += 1
                        '''print "Should be: ", list_tar,
                            print ", the result is: ", step_res'''
                    #print "error: ", error
print "total error:", tot_err
    print "total_correct:", corr_sum, ", accuracy: ", str(float(corr_sum) / float(len(dsTest['input'])))
