import json
import os
import random
import sys

def generate_data(file_tag, file_novels, file_tag_dev, file_novels_dev, file_tag_test, file_novels_test, file_tag_list, ratio=5):
    if ratio < 2:
        print('Invalid ratio! Ratio should be a integer graater than or eaqual to 2!')
        return
    
    counter = 0
    tag_dict = {}
    tag = open(file_tag, 'r')
    novels = [open(file_novel, 'r') for file_novel in file_novels]
    tag_dev = open(file_tag_dev, 'w')
    novels_dev = [open(file_novel_dev, 'w') for file_novel_dev in file_novels_dev]
    tag_test = open(file_tag_test, 'w')
    novels_test = [open(file_novel_test, 'w') for file_novel_test in file_novels_test]
    tag_list = open(file_tag_list, 'w')
    for line_tag in tag:
        counter += 1
        if line_tag.rstrip() not in tag_dict:
            tag_dict[line_tag.rstrip()] = 1
        if counter == ratio:
            counter = 0
            tag_test.write(line_tag)
            for novel, novel_test in zip(novels, novels_test):
                novel_test.write(novel.readline())
        else:
            tag_dev.write(line_tag)
            for novel, novel_dev in zip(novels, novels_dev):
                novel_dev.write(novel.readline())
    tag_list.write(json.dumps(list(tag_dict.keys())))
    tag_list.write(os.linesep)
    tag.close()
    for novel in novels:
        novel.close()
    tag_dev.close()
    for novel_dev in novels_dev:
        novel_dev.close()
    tag_test.close()
    for novel_test in novels_test:
        novel_test.close()
    tag_list.close()
    

if __name__ == '__main__':
    if len(sys.argv) < 8 or len(sys.argv) > 9:
        print('Please run run3.py instead.')
    else:
        file_tag = sys.argv[1]
        file_novels = [sys.argv[2]]
        file_tag_dev = sys.argv[3]
        file_novels_dev = [sys.argv[4]]
        file_tag_test = sys.argv[5]
        file_novels_test = [sys.argv[6]]
        file_tag_list = sys.argv[7]
        if len(sys.argv) == 9:
            ratio = int(sys.argv[8])
            generate_data(file_tag, file_novels, file_tag_dev, file_novels_dev, file_tag_test, file_novels_test, file_tag_list, ratio)
        else:
            generate_data(file_tag, file_novels, file_tag_dev, file_novels_dev, file_tag_test, file_novels_test, file_tag_list)
