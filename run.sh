echo tags file: $1
echo novels file: $2

echo Segmenting: ${2}...
python3 segment_word3.py $2 ${2}.seg
echo $2 segmented and output to ${2}.seg

echo Generating learning data...
python3 generate_data3.py $1 ${2}.seg ${1}.dev ${2}.dev ${1}.test ${2}.test ${1}.list
echo Learning data generated: ${1}.dev ${2}.dev ${1}.test ${2}.test

echo Learning NB model...
python3 nblearn3.py ${2}.dev ${1}.dev ${2}.model ${1}.list
echo NB model learned: ${2}.model

echo Classifying test data...
python3 nbclassify3.py ${2}.test ${2}.model ${2}.out ${2}.prob
echo Test data classfied: ${2}.out
echo Probability saved to ${2}.prob

echo Checking accuracy...
python3 check_accuracy3.py ${1}.test ${2}.out

echo Task completed.
