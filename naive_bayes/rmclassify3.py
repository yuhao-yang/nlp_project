# Zixuan Zhang
# 170428
# Random model: baseline
# input: tag probabilities, any feature file
# ouput: tag assignment

import json
import sys
import io
import os
import random

# assign tag for each file in input file
def apply(prob_path, input_path, output_path):
    probs = {}
    tags = []
    # read probabilities to file
    with open(prob_path, 'r', encoding = 'utf-8') as prob_file:
        probs = json.loads(prob_file.readline().rstrip())

    # assign tags
    with open(input_path, 'r') as in_file:
        while in_file.readline():
            score = {}
            for tag, prob in probs.items():
                score[tag] = random.random() ** (1 / prob)
            tags.append(max(score, key = lambda k: score[k]))

    # write to file
    with open(output_path, 'w') as out_file:
        for tag in tags:
            out_file.write(tag)
            out_file.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('inpur error! format: ')
        print('python random.py training_tag_file_path testing_any_feature_file_path output_file_path')
        sys.exit()
    
    training_path = sys.argv[-3]
    test_path = sys.argv[-2]
    output_file_path = sys.argv[-1]

    train(training_path, 'data/random_feature.txt')
    apply('data/random_feature.txt', test_path, )
