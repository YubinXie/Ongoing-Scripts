import re;
import os;
import sys, optparse;
import timeit;
import numpy;
start = timeit.default_timer()

usage="python xx.py inputfile out"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
InputFile=infile[0]
OutputFile=infile[1]
OpenoutFile=open(OutputFile,"w+")
RowNumber=0
with open(InputFile,"r") as OpenInputFile:
	for row in OpenInputFile:
		RowNumber+=1
		if RowNumber==1:
			continue
		ElementList=row.strip("\n").split("\t")
		BedInformation="\t".join(ElementList[0:3])
		ElementList=[float(i) for i in ElementList[4:]]
		MeanExpressionLevel=numpy.mean(ElementList[4:])
		OpenoutFile.write("%s\t%s\n" % (BedInformation,MeanExpressionLevel))

