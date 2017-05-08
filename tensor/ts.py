import ast
import operator

def f(x,dic):
    sorted_x = sorted(x.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    return str(dic[sorted_x[0][0]])

aa = open('tag4.txt.list').read()
aa = ast.literal_eval(aa)
dic = {}

for i in range(len(aa)):
    dic[aa[i]] = i+1

a = open('tag4.txt.test').readlines()
#a = [ast.literal_eval(item) for item in a]
#t = [f(item,dic) for item in a]

b = open('tag.txt','w')
a = [item.strip() for item in a]
for item in a:
    b.write(str(dic[item]) + '\n')

b.close()
