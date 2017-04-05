# encoding=utf-8
import jieba
import os

title_file_in = 'title.txt'
abstract_file_in = 'abstract.txt'
content_file_in = 'content.txt'
title_file_out = 'title_segmented.txt'
abstract_file_out = 'abstract_segmented.txt'
content_file_out = 'content_segmented.txt'

def segment(file_in, file_out):
    with open(file_in, 'r') as fin, open(file_out, 'w') as fout:
        for line_in in fin:
            seg_list = jieba.cut(line_in, cut_all=False)
            line_out = ' '.join(seg_list)
            fout.write(line_out)
            fout.write(os.linesep)
    fin.close()
    fout.close()

segment(title_file_in, title_file_out)
segment(abstract_file_in, abstract_file_out)
segment(content_file_in, content_file_out)
