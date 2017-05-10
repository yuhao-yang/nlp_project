import sys

def check_accuracy(file_name_ans, file_name_out):
    num_of_reviews = 0
    correct_count = 0
    
    with open(file_name_ans, 'r') as ans, open(file_name_out, 'r') as output:
        for ans_line, output_line in zip(ans, output):
            num_of_reviews += 1
            if ans_line == output_line:
                correct_count += 1
    ans.close()
    output.close()

    print('comparing ' + file_name_ans + ' and ' + file_name_out + ': ')
    print(correct_count, 'out of', num_of_reviews, 'novels are classified correctly.')
    print('the accuracy is', correct_count / num_of_reviews)

if __name__ == '__main__':
    file_name_ans = sys.argv[-2]
    file_name_out = sys.argv[-1]
    
    check_accuracy(file_name_ans, file_name_out)
