import copy
import json
import math
import os
import string
import sys

file_name_novels = sys.argv[-3]
file_name_parameters = sys.argv[-2]
file_name_output = sys.argv[-1]
prior_probabilities = {}
probabilities = {}
punctuations = string.punctuation + '+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-【】'

# Read parameters from file.
with open(file_name_parameters, 'r') as f:
    prior_probabilities = json.loads(f.readline().rstrip())
    probabilities = json.loads(f.readline().rstrip())
f.close()

# Read reviews from file.
with open(file_name_novels, 'r') as novels, open(file_name_output, 'w') as output:
    for line in novels:
        probability = copy.deepcopy(prior_probabilities)
        for token in line.rstrip().split():
            word = token.rstrip(punctuations).lower()
            if word and word in probabilities:
                for tag in prior_probabilities:
                    probability[tag] += probabilities[word][tag]
        tag = max(probability, key=probability.get)
        output.write(tag)
        output.write(os.linesep)
novels.close()
output.close()
