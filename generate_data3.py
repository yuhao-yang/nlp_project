import os
import random
import sys

def generate_data(file_tag, file_novels, file_tag_dev, file_novels_dev, file_tag_test, file_novels_test):

    data = []
    
    tag = open(file_tag, 'r')
    novels = [open(file_novel, 'r') for file_novel in file_novels]
    for line_tag in tag:
        line_data = [line_tag]
        for novel in novels:
            line_data.append(novel.readline())
        data.append(line_data)
    tag.close()
    for novel in novels:
        novel.close()
    
    random.shuffle(data)
    
    # 80% of data for training.
    tag = open(file_tag_dev, 'w')
    novels = [open(file_novel_dev, 'w') for file_novel_dev in file_novels_dev]
    for i in range(int(0.8 * len(data))):
        tag.write(data[i][0])
        for j in range(len(novels)):
            novels[j].write(data[i][1 + j])
    tag.close()
    for novel in novels:
        novel.close()
    
    # 20% of data fot testing.
    tag = open(file_tag_test, 'w')
    novels = [open(file_novel_test, 'w') for file_novel_test in file_novels_test]
    for i in range(int(0.8 * len(data)), len(data)):
        tag.write(data[i][0])
        for j in range(len(novels)):
            novels[j].write(data[i][1 + j])
    tag.close()
    for novel in novels:
        novel.close()

if __name__ == '__main__':
    print(sys.argv)
    num_of_features = 1
    start = 0
    if (len(sys.argv) > 7):
        num_of_features = sys.argv[1]
        start = 1
    file_tag = sys.argv[start + 1]
    file_novels = sys.argv[start + 2:start + 2 + num_of_features]
    file_tag_dev = sys.argv[start + 2 + num_of_features]
    file_novels_dev = sys.argv[start + 2 + num_of_features + 1: start + 2 + 2 * num_of_features + 1]
    file_tag_test = sys.argv[start + 2 + 2 * num_of_features + 1]
    file_novels_test = sys.argv[start + 2 + 2 * num_of_features + 2:start + 2 + 3 * num_of_features + 2]
    
    generate_data(file_tag, file_novels, file_tag_dev, file_novels_dev, file_tag_test, file_novels_test)
