#!/usr/bin/python

ref="arth.pep"
pos="arth.env"
Dic = {}


with open(ref) as f:
    for line in f:
        line = line.strip()
        if line.startswith('>'):
            k = line.split(' ',1)[0][1:]
            seq = ''
        else:
            seq += line
        Dic[k] = seq
            


          
with open(pos) as f:
    for line in f:
        line = line.split()
        ID = line[0]
        start = int(line[1])
        end = int(line[2])
        for k in Dic.keys():
            if k ==  ID:
                sequence = Dic[k][start-1:end]
                print '>%s\n%s' % (ID,sequence) 
     
