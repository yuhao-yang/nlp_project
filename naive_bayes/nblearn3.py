import json
import math
from numpy import array, argpartition
import os
import string
import sys

def nblearn(file_name_novels, file_name_tags, file_name_parameters, file_tag_list):
    # All English and Chinese punctuations
    punctuations = string.punctuation + '+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-【】'
    # Record the number of novels in training the data.
    num_of_novels = 0
    # Record the number of occurences for given word and tag after smoothing. Access with word_count[word][tag].
    word_count = {}
    # List all tags in training data.
    tags = []
    with open(file_tag_list, 'r') as tag_list:
        tags = json.loads(tag_list.readline().rstrip())
    tag_list.close()
    # Record the number of words for each tag after smoothing.
    num_of_words = dict.fromkeys(tags, 0)
    # Record the number of reviews belongs to each tag.
    tag_count = dict.fromkeys(tags, 1)
    
    # Read title/abstract/content and tags from files and count words.
    with open(file_name_novels, 'r') as novels_in, open(file_name_tags, 'r') as tags_in:
        for line in novels_in:
            num_of_novels += 1
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
    prior_probabilities = {tag : math.log2(tag_count[tag] / num_of_novels) for tag in tags}
    probabilities = {word : {tag : math.log2(word_count[word][tag] / num_of_words[tag]) for tag in tags} for word in word_count}
    
    # Write parameters to file.
    with open(file_name_parameters, 'w') as f:
        f.write(json.dumps(prior_probabilities))
        f.write(os.linesep)
        f.write(json.dumps(probabilities))
        f.write(os.linesep)
    f.close()

if __name__ == '__main__':
    # Read file names from commond line.
    file_name_novels = sys.argv[-4]
    file_name_tags = sys.argv[-3]
    file_name_parameters = sys.argv[-2]
    file_name_tag_list = sys.argv[-1]
    
    nblearn(file_name_novels, file_name_tags, file_name_parameters, file_name_tag_list)
