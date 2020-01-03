#!/usr/bin/python
#the script for extract gene, up stream, down stream from genome;The input file include gene ID line by line
#python version: python3
#History:
#   2020-1-3 v4 gossie

genome='/home/liuqb/data/genome/Cotton/HAU1.0/HAU_genome.fa'
gene='gene.txt'
GFF='/home/liuqb/data/genome/Cotton/HAU1.0/HAU.gene.gff3'
up=2000
down=2000

import re
genome_dic = {}

#参考序列词典
with open(genome,'r') as fa:
    for line in fa:
        line = line.strip()
        if line.startswith('>'):
            chr_id = line[1:]
            genome_dic[chr_id] = ''
        else:
            genome_dic[chr_id] += line
        print('dic ok')


#定义函数，Reverse Complement
def rev_comp(seq):
     base_trans = {'A':'T', 'C':'G', 'T':'A', 'G':'C', 'a':'t', 'c':'g', 't':'a', 'g':'c'}
     rev_seq = list(reversed(seq))
     rev_comp_seq_list = [base_trans[k] for k in rev_seq]
     rev_comp_seq = ''.join(rev_seq_list)
     return(rev_comp_seq)

with open(gene,'r') as gene_list:
    for geneid in gene_list:
        geneid=geneid.strip()
        with open(GFF,'r') as gff:
            for line in gff:
                line_list = line.strip().split()
                if geneid in line_list[8] and line_list[2]=='gene' and line_list[7]=='+':
                    chr=line_list[0]
                    gene_start=int(line_list[3])
                    gene_end=int(line_list[4])
                    up_start=int(int(line_list[3])-up)
                    down_end=int(int(line_list[4])+down)
                    print('1ok')
                    for key in genome_dic.keys():
                        if key == chr:
                            gene_sequence=genome_dic[key][gene_start-1:gene_end]
                            up_stream=genome_dic[key][up_start-1:gene_start]
                            down_stream=genome_dic[key][gene_end:down_end]
                            up_stream=rev_comp(genome_dic[key][gene_end:down_end])
                            print ('>%s\t%s-%s\t%s\n%s\n>%s\t%s-%s\t%s\n%s\n>%s\t%s-%s\t%s\n%s' %(geneid,gene_start,gene_end,line_list[7],gene_sequence,geneid+"_up",up_start,gene_start-1,line_list[7],up_stream,geneid+"_down",gene_end+1,down_end,line_list[7],down_stream))
                elif geneid in line_list[8] and line_list[2]=='gene' and line_list[7]=='-':
                    chr=line_list[0]
                    gene_start=int(line_list[3])
                    gene_end=int(line_list[4])
                    down_start=int(int(line_list[3])-down) #负链基因的下游在左端
                    up_end=int(int(line_list[4])+up)	   #负链基因的上游在右端
                    print('2ok')
                    for key in genome_dic.keys():
                        if key == chr:
                            gene_sequence=rev_comp(genome_dic[key][gene_start-1:gene_end])	#负链上的序列都要反向互补
                            down_stream=rev_comp(genome_dic[key][down_start-1:gene_start])
                            up_stream=rev_comp(genome_dic[key][gene_end:down_end])
                            print ('>%s\t%s-%s\t%s\n%s\n>%s\t%s-%s\t%s\n%s\n>%s\t%s-%s\t%s\n%s' %(geneid,gene_start,gene_end,line_list[7],gene_sequence,geneid+"_up",gene_end+1,up_end,line_list[7],up_stream,geneid+"_down",down_start,gene_start-1,line_list[7],down_stream))



