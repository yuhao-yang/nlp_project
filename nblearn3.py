import json
import math
from numpy import array, argpartition
import os
import string
import sys

# Read file names from commond line.
file_name_novels = sys.argv[-3]
file_name_tags = sys.argv[-2]
file_name_parameters = sys.argv[-1]

# Initializations.
punctuations = string.punctuation + '+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-【】'
# Record the number of reviews in training the data.
num_of_reviews = 0
# Record the number of words for each tag after smoothing.
num_of_words = {'city' : 0, 'sports' : 0, 'kongfu' : 0, 'ACG' : 0}
# Record the number of reviews belongs to each tag.
tag_count = {'city' : 0, 'sports' : 0, 'kongfu' : 0, 'ACG' : 0}
# Record the number of occurences for given word and tag after smoothing. Access with word_count[word][tag].
word_count = {}

# Read title/abstract/content and tags from files and count words.
with open(file_name_novels, 'r') as novels_in, open(file_name_tags, 'r') as tags_in:
    for line in novels_in:
        num_of_reviews += 1
        tag = tags_in.readline().rstrip()
        tag_count[tag] += 1
        
        for token in line.rstrip().split():
            word = token.rstrip(punctuations).lower()
            if word:
                num_of_words[tag] += 1
                if word not in word_count:
                    word_count[word] = {}
                    for t in tag_count:
                        word_count[word][t] = 1
                        num_of_words[t] += 1
                word_count[word][tag] += 1
                num_of_words[tag] += 1
novels_in.close()
tags_in.close()

# Construct NB model.
prior_probabilities = {tag : math.log2(tag_count[tag] / num_of_reviews) for tag in tag_count}
probabilities = {word : {tag : math.log2(word_count[word][tag] / num_of_words[tag]) for tag in tag_count} for word in word_count}

# Write parameters to file.
with open(file_name_parameters, 'w') as f:
    f.write(json.dumps(prior_probabilities))
    f.write(os.linesep)
    f.write(json.dumps(probabilities))
    f.write(os.linesep)
f.close()
