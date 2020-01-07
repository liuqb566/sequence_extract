#!/usr/bin/env python

#注释文件 
anno='/home/liuqb/data/genome/Cotton/HAU1.1/HAU_annotation_v1.1.txt'

gene="ld_gene.id"

with open(gene,'r') as fd:
    for query in fd:
        with open(anno,'r') as fe:
            for line in fe:
                if query.strip() in line.split()[0]:
                    print(query.strip(),line,sep='\t')
                    break
            
