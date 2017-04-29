# Zixuan Zhang
# 170428
# Random model: baseline
# input: tag files
# ouput: tag probabilities

import json
import sys
import io
import os
import random

# get probability for each tag in the input file
def train(input_path, output_path):
    # get probabilities from tag file
    probs = {}  # prob: {tag: tag_num}
    with open(input_path, 'r', encoding = 'utf-8') as tag_file:
        num = 0
        for line in tag_file:
            num += 1
            try:
                probs[line] += 1
            except KeyError:
                probs[line] = 1

    for tag, tag_num in probs.items():
        probs[tag] = float(tag_num) / float(num)

    # write probabilities to file
    with open(output_path, 'w') as out_file:
        out_file.write(json.dumps(probs))
        out_file.write(os.linesep)

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
