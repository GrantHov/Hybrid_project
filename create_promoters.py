#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:02:07 2017

@author: ghovhannisyan
"""

import sys
import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Seq import reverse_complement

prom_len=1000

with open(sys.argv[1], "r+") as gff_file:
	gff_dict={}
	for line in gff_file:
		if not line.startswith("#"):
			line=line.rstrip().split("\t")
			if line[2]=="gene":
				coords=[]
				coords.extend([line[3],line[4]])
				gene_name=line[8].split(";")[0][9:-1]
				#print gene_name
				gff_dict[line[0]+"*"+gene_name+"*"+line[6]]=coords
	print len(gff_dict)			

	#~ for k,v in gff_dict.iteritems():
		#~ print k,v
#~ print len(gff_dict)
	
#gff_dict2=gff_dict

counter=0
n_short_genes=0
with open(sys.argv[2], "r") as genome, open(sys.argv[3], "w") as output:
	for record in SeqIO.parse(genome, "fasta"): 
		for gene,coords in gff_dict.iteritems():
			if gene.split("*")[0]==record.id:
					if gene.split("*")[2]=="+":
						if int(coords[0])>int(prom_len):
							overlap_counter=0
							max_coord=0
							for k,v in gff_dict.iteritems():
								if k.split("*")[0]!=gene.split("*")[1] and k.split("*")[0]==record.id and k.split("*")[2]=="+" and int(coords[0])-1000 <int(v[1])< int(coords[0]):
									counter+=1
									overlap_counter+=1
									if int(v[1])>max_coord:
										#print max_coord
										max_coord=int(v[1])
										#print max_coord
									#else:
									#	print "blah" # int(v[1])
									#~ print k,v, gene, coords
									#~ print int(int(coords[0])-50)
									#~ print int(v[1])
									#~ print int(coords[0])
							if overlap_counter>0:
								#print overlap_counter #, max_coord
								sequence=record.seq.tomutable()
								sequence=sequence[int(max_coord)+1:int(coords[0])-1]
								#print sequence, gene.split("*")[1], int(coords[0])-500, "this on +, normal"
								if len(sequence)>100:
									output.write(">%s=%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],int(max_coord)+1,int(coords[0])-1,len(sequence),gene.split("*")[2],"OVERLAPPED",sequence))
								else:
									n_short_genes+=1
							elif overlap_counter==0:
								sequence=record.seq.tomutable()
								sequence=sequence[int(coords[0])-int(int(prom_len)+1):int(coords[0])-1]
								#print sequence, gene.split("*")[1], int(coords[0])-500, "this on +, normal"
								if len(sequence)>100:	
									output.write(">%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],coords[0],coords[1],len(sequence),gene.split("*")[2],sequence))
								else:
									n_short_genes=+1
						elif int(coords[0])>50 and int(coords[0])<int(prom_len):
							overlap_counter=0
							max_coord=0
							for k,v in gff_dict.iteritems():
								if k.split("*")[0]!=gene.split("*")[1] and k.split("*")[0]==record.id and k.split("*")[2]=="+" and int(coords[0])-1000 <int(v[1])< int(coords[0]):
									counter+=1
									overlap_counter+=1
									if int(v[1])>max_coord:
										#print max_coord
										max_coord=int(v[1])
										#print max_coord
									#else:
									#	print "blah" # int(v[1])
									#~ print k,v, gene, coords
									#~ print int(int(coords[0])-50)
									#~ print int(v[1])
									#~ print int(coords[0])
							if overlap_counter>0:
								#print overlap_counter #, max_coord
								sequence=record.seq.tomutable()
								sequence=sequence[int(max_coord)+1:int(coords[0])-1]
								#print sequence, gene.split("*")[1], int(coords[0])-500, "this on +, normal"
								if len(sequence)>100:	
									output.write(">%s=%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],int(max_coord)+1,int(coords[0])-1,len(sequence),gene.split("*")[2],"OVERLAPPED_overflow",sequence))
								else:
									n_genes_short=+1
							elif overlap_counter==0:
								sequence=record.seq.tomutable()
								sequence=sequence[0:int(coords[0])-1]
								#print len(sequence), gene.split("*")[1], int(coords[0])-500, "this on +, short"
								if len(sequence)>100:
									output.write(">%s=%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],coords[0],coords[1],len(sequence),gene.split("*")[2],"overflow",sequence))
								else:
									n_short_genes+=1
					elif gene.split("*")[2]=="-":
						if int(coords[1])+int(prom_len)<=len(record.seq):
							overlap_counter_m=0
							min_coord=1000000000000000000000000
							for k,v in gff_dict.iteritems():
								if k.split("*")[0]!=gene.split("*")[1] and k.split("*")[0]==record.id and k.split("*")[2]=="-" and int(coords[1])<int(v[0])< int(coords[1])+int(prom_len):
									counter+=1
									#print "OVERLAP"
									overlap_counter_m+=1
									if int(v[0])<=min_coord:
										#print max_coord
										min_coord=int(v[0])
										#print max_coord
									#else:
									#	print "blah" # int(v[1])
									#~ print k,v, gene, coords
									#~ print int(int(coords[0])-50)
									#~ print int(v[1])
									#~ print int(coords[0])
							if overlap_counter_m>0:
								#print overlap_counter_m,int(coords[1]),int(min_coord)
								sequence=record.seq.tomutable()
								sequence=sequence[int(coords[1]):int(min_coord)]
								reverse_seq=reverse_complement(sequence)
								#print sequence, gene.split("*")[1], int(coords[0])-500, "this on +, normal"
								if len(sequence)>100:
									output.write(">%s=%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],int(coords[1]),int(min_coord),len(sequence),gene.split("*")[2],"OVERLAPPED",reverse_seq))
								else:
									n_short_genes+=1
							elif overlap_counter_m==0:
								sequence=record.seq.tomutable()
								sequence=sequence[int(coords[1]):int(coords[1])+int(prom_len)]
								reverse_seq=reverse_complement(sequence)
								#print reverse_seq
								#print reverse_seq, gene.split("*")[1],"this is on -, normal"
								if len(sequence)>100:
									output.write(">%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],int(coords[1]),int(coords[1])+int(prom_len),len(reverse_seq),gene.split("*")[2],reverse_seq))
								else:
									n_short_genes+=1
						elif int(coords[1])+int(prom_len)>len(record.seq):
							overlap_counter_m=0
							min_coord=100000000000000000000
							for k,v in gff_dict.iteritems():
								if k.split("*")[0]!=gene.split("*")[1] and k.split("*")[0]==record.id and k.split("*")[2]=="-" and int(coords[1])<int(v[0])< int(coords[1])+int(prom_len):
									counter+=1
									overlap_counter_m+=1
									if int(v[0])<min_coord:
										#print max_coord
										min_coord=int(v[0])
										#print max_coord
									#else:
									#	print "blah" # int(v[1])
									#~ print k,v, gene, coords
									#~ print int(int(coords[0])-50)
									#~ print int(v[1])
									#~ print int(coords[0])
							if overlap_counter_m>0:
								#print overlap_counter_m #, max_coord
								sequence=record.seq.tomutable()
								sequence=sequence[int(coords[1]):int(min_coord)]
								reverse_seq=reverse_complement(sequence)
								#print sequence, gene.split("*")[1], int(coords[0])-500, "this on +, normal"
								if len(sequence)>100:	
									output.write(">%s=%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],int(coords[1]),int(min_coord),len(sequence),gene.split("*")[2],"OVERLAPPED_overflow",reverse_seq))
								else:
									n_short_genes+=1
							elif overlap_counter_m==0:
								sequence=record.seq.tomutable()
								sequence=sequence[int(coords[1]):]
								reverse_seq=reverse_complement(sequence)
								#print reverse_seq, gene.split("*")[1], "this is on -, short"
								if len(reverse_seq)>100:
									output.write(">%s=%s=%s=%s=%s=%s=%s\n%s\n"%(record.id,gene.split("*")[1],coords[1],len(record.seq),len(reverse_seq),gene.split("*")[2],"overflow",reverse_seq))
								else:
									n_short_genes+=1
			else:
				continue
print n_short_genes
print counter