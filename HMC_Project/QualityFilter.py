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
	line2=re.search('(?P<h1>.+?)_(?P<h3>.+?)_all',File)
	if(line2):
		name1=line2.group("h1")
		name2=line2.group("h3")
		name=name1+"_"+name2
		if name not in GroupName:
			name1list.append(name1)
			name2list.append(name2)
			GroupName.append(name)	
	else: 
		print "no pattern found in this file:", File
	i=i+1
print GroupName

####################################3
commend="mkdir -p quality && "
#######cat differnt lanes into one file########
i=0
###############################################

for sample in GroupName:
	
	inputname=name1list[i]+"_"+name2list[i]+"_alllanes.fastq.gz"
	outputname="quality/"+name1list[i]+"_"+name2list[i]+"_merged_quality.fastq.gz"
	commend=commend+"gunzip -c " + inputname + " | ~/tools/fastx/fastq_quality_filter -q 20 -p 90 -z -Q33 -o "+ outputname + " && "  
	i=i+1
###############################################
commend=commend+ "ls "
print commend

process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode