#!/usr/bin/python

import sys, optparse
import timeit;
start = timeit.default_timer()
import subprocess

usage="python xx.py InputFile "
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

InputFile=infile[0]
Temp=InputFile.replace(".txt", "temp.txt")
OutPut=infile[0].replace(".txt",".fa")

InitialCommend="sort -k1n " + InputFile + " > " + Temp
process=subprocess.Popen(InitialCommend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode

with open (Temp, "r") as openInputFile, open (OutPut, "w+") as openOutputFile:
	LineNumber=0
	for Line in openInputFile:
		LineNumber+=1
		ElementList=Line.strip("\n").split("\t")
		Read=ElementList[0].strip(" ")
		openOutputFile.writelines( ">%s\n" % LineNumber)
		openOutputFile.writelines( "%s\n" % Read)
Commend="rm " + Temp
process=subprocess.Popen(Commend,shell=True,stdout=subprocess.PIPE)
process.wait()
print process.returncode

stop = timeit.default_timer()
print "Time used: ", stop - start,  