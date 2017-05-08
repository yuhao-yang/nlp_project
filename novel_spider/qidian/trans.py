# coding : utf-8

b = open('content2.txt','r').readlines();
a = open('title2.txt','r').readlines();

a = [item.strip() for item in a]
b = [item.strip() for item in b if item.strip() != '']
c = [item.split()[0] for item in b] 
d = [item.split()[1].strip() for item in b]
dic = {}

for i in range(len(c)):
    dic[c[i]] = d[i]

for item in a:
    if item not in dic:
        dic[item] = "null"

f = open('content.txt','w')

for item in a:
    f.write(dic[item] + '\n')

f.close()