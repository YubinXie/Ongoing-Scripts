import re;
import os
import sys, optparse

usage="python xx.py InputFile OutputFile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
OutputFile=open(infile[1],'w+')

InputLineNumber=0
NoIndelLineNumber=0
OutputLineNumber=0

with open(infile[0]) as inputfile:
	for line in inputfile:
		array=line.split("\t")
		if len(array)<=9:
			continue
		InputLineNumber+=1
		if array[5]=="125M":
			NoIndelLineNumber+=1
			Reads=array[9]
			Target=Reads[24:42]
			if "N" not in Target:
				OutputLineNumber+=1
				OutputContent=Target+"\n"
				OutputFile.write(OutputContent)
print infile[0], InputLineNumber, NoIndelLineNumber, OutputLineNumber
OutputFile.close()