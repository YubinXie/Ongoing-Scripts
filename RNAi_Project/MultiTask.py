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
GroupName=[]
NameList=[]
InputName=""
OutputName=""
############################
def main():
####Choose One#######
	#Mapping()
	Extraction()
	#Counting()
#####################

	MainPart()


def Mapping():
	global FilePattern,OutputFolder, OutputType, CommendLine1, CommendLine2
	FilePattern="_1.fa.gz"
	OutputFolder="sam"
	OutputType=".sam"
	CommendLine1="bowtie2 -p 8 -x /media/yubin/Alpha/sRNAProject/ReferenceGenome/L6sRNA150bp -k 1 -U "
	CommendLine2 = " --n-ceil L,0,0.25 -S "

def Extraction():
	global FilePattern,OutputFolder, OutputType, CommendLine1, CommendLine2
	FilePattern=".sam"
	OutputFolder="txt"
	OutputType=".txt"
	CommendLine1="python /home/yubin/Dropbox/Linux/scripts/RNAi_Project/Extraction.py "
	CommendLine2=" "

def Counting():
	global FilePattern, OutputFolder,OutputType, CommendLine1, CommendLine2
	FilePattern=".txt"
	OutputFolder="counts"
	OutputType="-counts.txt"
	CommendLine1="python /home/yubin/Dropbox/Linux/scripts/RNAi_Project/CountingRead.py "
	CommendLine2=" "

def MainPart():
	global FilePattern, OutputType, CommendLine1,CommendLine2
	############################
	i=1
	#####Catch the main sample name###### 
	for File in FileName: 
		line2=re.search('(?P<h1>.+?)'+FilePattern,File)
		if(line2):
			name=line2.group("h1")
			if name not in NameList:
				NameList.append(name)
				GroupName.append(File)
		else: 
			print "no pattern found in this file:", File
		i=i+1
	print NameList
	
	####################################
	
	####################################
	i=0
	InitialCommend="mkdir -p " + OutputFolder
	process=subprocess.Popen(InitialCommend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
	
	for sample in NameList:
		InputName = GroupName[i]
		OutputName= OutputFolder + "/"+NameList[i] + OutputType
		commend=CommendLine1 + InputName + CommendLine2 + OutputName
		print commend
		process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
		process.wait()
		print process.stdout.readlines()
		i=i+1
	##########################
	

if __name__ == '__main__':
	main()