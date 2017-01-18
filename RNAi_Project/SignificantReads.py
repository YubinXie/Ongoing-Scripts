#!/usr/bin/python

import sys, optparse
import timeit;
start = timeit.default_timer()

usage="python xx.py ControlFile CaseFile OutputFile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

ControlDic = {}

with open(infile[0],"r") as ControlFile:
	for Line in ControlFile:
		ElementList = Line.split("\t").strip("\n")
		ControlDic[ElementList[0]] = int(ElementList[1])

with open(infile[1],"r") as CoaselFile, open (infile[2],"w+") as OutputFile :
	for Line in CaseFile:
		ElementList = Line.split("\t").strip("\n")
		Reads = ElementList[0]
		CaseCounts = ElementList[1]
		if Reads not in ControlDic:
			ControlCounts = 0
			Pvalue =

		else:
			CaseCounts = ControlDic[Reads]
			Pvalue =

		OutputFile.writelines('%s\t%s\t%s\n' % (Reads,ControlCounts,CaseCounts,Pvalue))



print "Time used: ", stop - start,    