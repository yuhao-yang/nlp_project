# encoding=utf-8
import jieba
import os
import sys

def segment(file_in, file_out):
    with open(file_in, 'r') as fin, open(file_out, 'w') as fout:
        for line_in in fin:
            seg_list = jieba.cut(line_in.rstrip(), cut_all=False)
            line_out = ' '.join(seg_list)
            fout.write(line_out)
            fout.write(os.linesep)
    fin.close()
    fout.close()

if __name__ == '__main__':
    file_in = sys.argv[-2]
    file_out = sys.argv[-1]
    
    segment(file_in, file_out)
    