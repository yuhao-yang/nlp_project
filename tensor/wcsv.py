import csv
a = open('title.txt').readlines()
b = open('abs.txt').readlines()
c = open('content.txt').readlines()
d = open('tag.txt').readlines()

a = [item.strip() for item in a]
b = [item.strip() for item in b]
c = [item.strip() for item in b]
d = [item.strip() for item in d]

f1 = open('data1.csv','w')
w = csv.writer(f1, delimiter=',')

for i in range(3300):
    data = [int(a[i])-1,int(b[i])-1,int(c[i])-1,int(d[i])-1]
    w.writerow(data)
f1.close()

f2 = open('test1.csv','w')
w = csv.writer(f2, delimiter=',')

for i in range(3300,len(a)):
    data = [int(a[i])-1,int(b[i])-1,int(c[i])-1,int(d[i])-1]
    w.writerow(data)
f2.close()