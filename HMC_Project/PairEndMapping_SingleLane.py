import re;
import os
import sys, optparse
import subprocess

usage="python xx.py infile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
FileName = os.listdir(infile[0])
print FileName 
os.chdir(infile[0])
#sum=0
GroupName=[]
name1list=[]
i=1
#####Catch the main sample name###### 
for File in FileName: 
	line2=re.search('(?P<h1>.+?)_R(?P<h2>.+?)001.fastq',File)
	if(line2):
		name1=line2.group("h1")
		if name1 not in name1list:
			name1list.append(name1)
	else: 
		print "no pattern found in this file:", File
	i=i+1
print name1list

####################################3

#######cat differnt lanes into one file########
i=0
commend=""
for sample in name1list:
	
	input1name=name1list[i]+"_R1*_001.fastq.gz"
	input2name=name1list[i]+"_R2*_001.fastq.gz"
	outputname=name1list[i]+"_paired.sam"
	commend=commend+"bowtie2 -p 8 -x /media/yubin/Alpha/reference/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.bowtie_index -1 " + input1name + " -2 " + input2name + " -S " + outputname + " && "  
	i=i+1
##########################
commend=commend+ "ls"
print commend

process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode
