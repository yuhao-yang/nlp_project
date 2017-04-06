import sys

from check_accuracy3 import check_accuracy
from generate_data3 import generate_data
from nbclassify3 import nbclassify
from nblearn3 import nblearn
from segment_word3 import segment

SEG = '.seg'
DEV = '.dev'
TEST = '.test'
MODEL = '.model'
OUT = '.out'
PROB = '.prob'

file_name_tag = sys.argv[1]
file_name_novels = sys.argv[2:]

for file_name_novel in file_name_novels:
    segment(file_name_novel, file_name_novel + SEG)
generate_data(
    file_name_tag,
    [file_name_novel + SEG for file_name_novel in file_name_novels],
    file_name_tag + DEV,
    [file_name_novel + DEV for file_name_novel in file_name_novels],
    file_name_tag + TEST,
    [file_name_novel + TEST for file_name_novel in file_name_novels])
    
for file_name_novel in file_name_novels:
    nblearn(file_name_novel + DEV, file_name_tag + DEV, file_name_novel + MODEL)
    nbclassify(file_name_novel + TEST, file_name_novel + MODEL, file_name_novel + OUT, file_name_novel + PROB)
    check_accuracy(file_name_tag + TEST, file_name_novel + OUT)