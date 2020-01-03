#!/usr/bin/python
#the script for extract gene, up stream, down stream from genome;The input file include gene ID line by line
#python version: python3
#History:
#   2020-1-3 v4 gossie

#基因组文件
genome='/home/liuqb/data/genome/Cotton/HAU1.0/HAU_genome.fa'
#注释文件，GFF3格式
GFF='/home/liuqb/data/genome/Cotton/HAU1.0/HAU.gene.gff3'
#基因 ID
gene='gene.txt'
#上游碱基数（默认从5‘UTR之前开始计算）
up=2000
#下游碱基数(默认从3’UTR之后开始计算)
down=2000

import re
genome_dic = {}

#参考序列词典
with open(genome,'r') as fa:
    for line in fa:
        line = line.strip()
        if line.startswith('>'):
            chr_id = line[1:]
            genome_dic[chr_id] = []
        else:
            genome_dic[chr_id].append(line)
    for key,value in genome_dic.items():
        genome_dic[key]=''.join(value)

#定义函数，Reverse Complement，对负链上的基因反向互补
def rev_comp(seq):
     base_trans = {'A':'T', 'C':'G', 'T':'A', 'G':'C', 'a':'t', 'c':'g', 't':'a', 'g':'c'}
     rev_seq = list(reversed(seq))
     rev_comp_seq_list = [base_trans[k] for k in rev_seq]
     rev_comp_seq = ''.join(rev_comp_seq_list)
     return(rev_comp_seq)

with open(gene,'r') as gene_list:
    for geneid in gene_list:
        geneid=geneid.strip()
        with open(GFF,'r') as gff:
            for line in gff:
                line=line.strip()
                line_list=line.split()
                if not line.startswith("#") and geneid in line_list[8] and line_list[2]=='gene' and line_list[6]=='+':
                    gene_start=int(line_list[3])
                    gene_end=int(line_list[4])
                    up_start=int(int(line_list[3])-up)
                    down_end=int(int(line_list[4])+down)
                    chr_seq=genome_dic.get(line_list[0],"Chr name erro")	#字典的get()函数
                    gene_sequence=chr_seq[gene_start-1:gene_end]
                    up_stream=chr_seq[up_start-1:gene_start]
                    down_stream=chr_seq[gene_end:down_end]
                    print ('>%s %s-%s %s\n%s\n>%s %s-%s %s\n%s\n>%s %s-%s %s\n%s' %(geneid,gene_start,gene_end,line_list[6],gene_sequence,geneid+"_up",up_start,gene_start-1,line_list[6],up_stream,geneid+"_down",gene_end+1,down_end,line_list[6],down_stream))
                    break 
                elif not line.startswith("#") and geneid in line_list[8] and line_list[2]=='gene' and line_list[6]=='-':
                    gene_start=int(line_list[3])
                    gene_end=int(line_list[4])
                    down_start=int(int(line_list[3])-down) #负链基因的下游在左端
                    up_end=int(int(line_list[4])+up)	   #负链基因的上游在右端
                    chr_seq=genome_dic.get(line_list[0],"Chr name erro")
                    gene_sequence=rev_comp(chr_seq[gene_start-1:gene_end])	#负链上的序列都要反向互补
                    down_stream=rev_comp(chr_seq[down_start-1:gene_start])
                    up_stream=rev_comp(chr_seq[gene_end:up_end])
                    print ('>%s %s-%s %s\n%s\n>%s %s-%s %s\n%s\n>%s %s-%s %s\n%s' %(geneid,gene_start,gene_end,line_list[6],gene_sequence,geneid+"_up",gene_end+1,up_end,line_list[6],up_stream,geneid+"_down",down_start,gene_start-1,line_list[6],down_stream))
                    break

