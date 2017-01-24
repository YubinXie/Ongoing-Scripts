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
NameList=[]
############################

############################
i=1
#####Catch the main sample name###### 
for File in FileName: 
	line2=re.search('(?P<h1>.+?)_1.fq.gz',File)
	if(line2):
		name=line2.group("h1")
		if name not in NameList:
			NameList.append(name)
			GroupName.append(File)
	else: 
		print "no pattern found in this file:", File
	i=i+1
print NameList

####################################3

#######cat differnt lanes into one file########
i=0
commend="mkdir -p sam"

process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode

for sample in NameList:
	InputName = GroupName[i]
	OutputName="sam/"+NameList[i]+".sam"


	commend="bowtie2 -p 8 -x /media/yubin/Alpha/sRNAProject/referenceGenome/L6sRNA150bp -k 1 -U " + InputName + " --n-ceil L,0,0.25 -S " + OutputName
	print commend
	process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
	
	i=i+1
##########################

