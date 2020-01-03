#!/usr/bin/python

#上游
up=2000
#下游
down=2000
#注释文件
GFF='/home/liuqibao/workspace/research/database/genome/NAU_replace.gff3'
# snp 文件
SNP='/home/liuqibao/workspace/research/chl_数据处理/355材料/GWAS_355/gemma_based/re-sequencing/SPAD_含量/sig_th10.txt'
import re

with open(SNP,'r') as fd1:
    for line in fd1:
        chromosome = line.strip().split("\t")[1]
        pos = line.strip().split("\t")[2]
        with open(GFF,'r') as fd2:
            for ll in fd2:
                ll_list = ll.split()
                if chromosome == ll_list[0] and int(ll_list[3]) > (int(pos)-up) and int(ll_list[4]) < (int(pos)+down) and ll_list[2]=='gene':
                    m = re.search(r'(Gh\w+\d+);',ll_list[8])
                    result = '%s\t%s\t%s\t%s' % (line.strip(),m.group(1),ll_list[3],ll_list[4])
                    print (result)



