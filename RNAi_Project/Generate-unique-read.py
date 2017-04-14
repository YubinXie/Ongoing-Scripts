#!/usr/bin/python

import sys, optparse
import timeit;
start = timeit.default_timer()
import subprocess

usage="python xx.py InputFile OutputFastaFile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

InputFile=infile[0]
Temp=InputFile.strip(".txt") + "temp.txt"


InitialCommend="sort -k1n " + InputFile + " > " + Temp
process=subprocess.Popen(InitialCommend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode

with open (Temp, "r") as openInputFile, open (infile[1], "w+") as openOutputFile:
	LineNumber=0
	for Line in openInputFile:
		LineNumber+=1
		ElementList=Line.split("\t")
		Read=ElementList[0]
		openOutputFile.writelines( ">%s\n" % LineNumber)
		openOutputFile.writelines( "%s\n" % Read)
Commend="rm " + Temp
process=subprocess.Popen(Commend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode

stop = timeit.default_timer()
print "Time used: ", stop - start,  