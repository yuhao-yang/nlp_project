a = open('title.txt').readlines()
b = open('abs.txt').readlines()
c = open('content.txt').readlines()
d = open('tag.txt').readlines()

a = [item.strip() for item in a]
b = [item.strip() for item in b]
c = [item.strip() for item in c]
d = [item.strip() for item in d]

la = len([1 for i in range(len(a)) if a[i] == d[i]])
lb = len([1 for i in range(len(b)) if b[i] == d[i]]) 
lc = len([1 for i in range(len(c)) if c[i] == d[i]]) 
print 'line 15 ' + str(la) + ' ' + str(lb) + ' ' + str(lc)
