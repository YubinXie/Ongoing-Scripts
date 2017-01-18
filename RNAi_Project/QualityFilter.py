import re;
import os
import sys, optparse
import subprocess

usage="python xx.py directory"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
FileName = os.listdir(infile[0])
print FileName 
os.chdir(infile[0])
#sum=0
GroupName=[]
name1list=[]
name2list=[]
i=1
#####Catch the main sample name###### 
for File in FileName: 
	line2=re.search('(?P<h1>.+?)_1.fq.gz',File)
	if(line2):
		name1=line2.group("h1")
		if name1 not in name1list:
			name1list.append(name1)
			GroupName.append(File)
	else: 
		print "no pattern found in this file:", File
	i=i+1
print name1list

####################################3
commend="mkdir -p quality"
print commend
process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode
#######cat differnt lanes into one file########
i=0
###############################################

for sample in GroupName:
	inputname=name1list[i] + "_1.fq.gz"
	outputname="quality/"+name1list[i]+"_quality.fastq.gz"
	commend="gunzip -c " + inputname + " | ~/tools/fastx/fastq_quality_filter -q 20 -p 90 -z -o "+ outputname 
	i=i+1
	print commend
	process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
###############################################

