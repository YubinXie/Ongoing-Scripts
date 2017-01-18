import re;
import os
import sys, optparse
import subprocess

usage="python xx.py file_directory script_directory "
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
FileNameList = os.listdir(infile[0])
WorkDirectory=infile[0]
ScriptDirectory=infile[1]
print FileNameList, WorkDirectory, ScriptDirectory 
os.chdir(infile[0])

#####Task one: Merge Lanes##########
def MergeLanes():
	commend1="python " + ScriptDirectory +"MergeLanes.py " + WorkDirectory
	print commend1
	process=subprocess.Popen(commend1,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
#####Task two: Quality Filter#######
def QualityControl():
	commend2="python " + ScriptDirectory +"QualityFilter.py " + WorkDirectory
	print commend2
	process=subprocess.Popen(commend2,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
#####Task three: Equal Reads after Quality FIlter#######
def EqualReads():
	commend3="python " + ScriptDirectory +"EqualReads.py " + WorkDirectory + "quality"
	print commend3
	process=subprocess.Popen(commend3,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
#####Task four: Mapping#######
def PairEndMapping():
	commend4="python " + ScriptDirectory +"PairEndMapping.py " + WorkDirectory + "quality"
	print commend4
	process=subprocess.Popen(commend4,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.returncode

def main():
	#MergeLanes()
	#QualityControl()
	EqualReads()
	PairEndMapping()
main()
