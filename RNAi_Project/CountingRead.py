#!/usr/bin/python
import subprocess
import sys, optparse
import timeit;
start = timeit.default_timer()

usage="python xx.py Inputfile Outputfile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
InputReadsNumber=0
ReadsNumber=0
ReadsList=[]
ReadsDic={}
TempFile="TempFile.txt"

with open(infile[0]) as InputFile:
	for Line in InputFile:
		InputReadsNumber+=1
		Line=Line.strip("\n")
		if Line not in ReadsDic:
			ReadsDic[Line]=1
		else:
			ReadsDic[Line]+=1

with open (TempFile, "w+") as OpenTempFile:
	OutputLine=0
	for key, value in ReadsDic.items():
		if value>=2:
			OpenTempFile.writelines('%s\t%s\n' % (key,value))
			OutputLine+=1
		ReadsNumber = ReadsNumber + value

commend="sort -nk2 -r " + TempFile + " > " + infile[1]
process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
process.wait()
commend="rm " + TempFile
process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)

stop = timeit.default_timer()
print "Done; \nInputfile line number:", InputReadsNumber, "\nCount reads number in output file: ", ReadsNumber,"Total Unique Reads",len(ReadsDic.items()) ,"\nOutputfile line number (reads>=2):", OutputLine
print "Time used: ", stop - start,    	