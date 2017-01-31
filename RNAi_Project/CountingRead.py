#!/usr/bin/python

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

with open(infile[0]) as InputFile:
	for Line in InputFile:
		InputReadsNumber+=1
		Line=Line.strip("\n")
		if Line not in ReadsDic:
			ReadsDic[Line]=1
		else:
			ReadsDic[Line]+=1

with open (infile[1], "w+") as OutputFile:
	OutputLine=0
	for key, value in ReadsDic.items():
		if value>=2:
			OutputFile.writelines('%s\t%s\n' % (key,value))
			OutputLine+=1
		ReadsNumber = ReadsNumber + value

stop = timeit.default_timer()
print "Done; \nInputfile line number:", InputReadsNumber, "\nCount reads number in output file: ", ReadsNumber,"Total Reads",len(ReadsDic.items()) ,"\nOutputfile line number (reads>=2)", OutputLine
print "Time used: ", stop - start,    	