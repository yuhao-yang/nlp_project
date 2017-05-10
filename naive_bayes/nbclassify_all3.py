import copy
import json
import math
import os
import string
import sys

def nbclassify_all(file_name_novels, file_name_parameters, file_name_output, file_name_probability):
    prior_probabilities = {}
    probabilities = []
    punctuations = string.punctuation + '+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-【】'
    
    # Read parameters from file.
    parameters = [open(file_name_parameter, 'r') for file_name_parameter in file_name_parameters]
    for parameter in parameters:
        prior_probabilities = json.loads(parameter.readline().rstrip())
        probabilities.append(json.loads(parameter.readline().rstrip()))
        parameter.close()
    
    # Read novels from file.
    novels = [open(file_name_novel, 'r') for file_name_novel in file_name_novels]
    with open(file_name_output, 'w') as output, open(file_name_probability, 'w') as prob:
        finished = False
        while not finished:
            nb_probabilities = copy.deepcopy(prior_probabilities)
            for novel, probability in zip(novels, probabilities):
                line = novel.readline()
                if not line:
                    finished = True
                    break
                for token in line.rstrip().split():
                    word = token.rstrip(punctuations).lower()
                    if word and word in probability:
                        for tag in prior_probabilities:
                            nb_probabilities[tag] += probability[word][tag]
            if not finished:
                prob.write(json.dumps(nb_probabilities))
                prob.write(os.linesep)
                
                tag = max(nb_probabilities, key=nb_probabilities.get)
                output.write(tag)
                output.write(os.linesep)
    for novel in novels:
        novel.close()
    output.close()
    prob.close()
