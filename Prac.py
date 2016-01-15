import string

tosort = []
f = open('prac.txt','r')

listy = f.readlines()

for item in listy:
    tosort.append(item)


print(tosort)



