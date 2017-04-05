import os
import random
import sys

def generate_data(file_tag, file_novel, file_tag_dev, file_novel_dev, file_tag_test, file_novel_test):

    data = []
    
    with open(file_tag, 'r') as tag, open(file_novel, 'r') as novel:
        for line_tag in tag:
            line_novel = novel.readline()
            data.append([line_tag, line_novel])
    tag.close()
    novel.close()
    
    random.shuffle(data)
    
    # 80% of data for training.
    with open(file_tag_dev, 'w') as tag, open(file_novel_dev, 'w') as novel:
        for i in range(int(0.8 * len(data))):
            tag.write(data[i][0])
            novel.write(data[i][1])
    tag.close()
    novel.close()
    
    # 20% of data fot testing.
    with open(file_tag_test, 'w') as tag, open(file_novel_test, 'w') as novel:
        for i in range(int(0.8 * len(data)), len(data)):
            tag.write(data[i][0])
            novel.write(data[i][1])
    tag.close()
    novel.close()

if __name__ == '__main__':
    file_tag = sys.argv[-6]
    file_novel = sys.argv[-5]
    file_tag_dev = sys.argv[-4]
    file_novel_dev = sys.argv[-3]
    file_tag_test = sys.argv[-2]
    file_novel_test = sys.argv[-1]
    
    generate_data(file_tag, file_novel, file_tag_dev, file_novel_dev, file_tag_test, file_novel_test)
