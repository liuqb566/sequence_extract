#!/usr/bin/python
#History:
#	2019-1-6 V2 Gossie

import re

# fragment file，txt 文件，三列：染色体、起始位置、终止位置；无表头
ff="ldblocks.txt"
# 注释文件
gff="/home/liuqb/data/genome/Cotton/HAU1.0/HAU.gene.gff3"

#构建注释文件词典
gff_dic={}
with open (gff,'r') as gf:
    for line in gf:
        line_list=line.strip().split()
        if not line.startswith("#") and line_list[2]=='gene':
            gff_dic.setdefault(line_list[0],[]).append(line_list)

with open(ff,'r') as f:
    for line in f:
        line_list=line.strip().split()
        chromosome = line_list[0]
        start = line_list[1]
        end = line_list[2]
        for value in gff_dic[chromosome]:
            if int(value[4])<int(start) or int(value[3])>int(end):
                continue
            else:
                m=re.search(r'ID=(.*);',value[8])
                print("%s\t%s\t%s\t%s\t%s\t%s\t" %(chromosome,start,end,m.group(1),value[3],value[4]))
