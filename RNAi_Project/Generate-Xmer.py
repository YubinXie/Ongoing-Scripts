#!/usr/bin/python

import sys, optparse
import timeit;
start = timeit.default_timer()

usage="python xx.py Inputfile X(-mer)"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

Xmer=int(infile[1])
OutputFileName=infile[0].replace("19",str(Xmer))
ReadsNumber=0
if Xmer != 19: 
	with open(infile[0]) as InputFile, open (OutputFileName, "w+") as OutputFile:
		InputReadsNumber=0
		OutputFile.writelines('>TEST\n')
		OutputFile.writelines("AAAAAAAAAAAAAAAAAAAA\n")
		for Line in InputFile:
			InputReadsNumber+=1
			Line=Line.strip("\n")
			if ">" in Line:
				Number=Line.strip(">")				
			else:
				Read=Line
				for i in range(0,20-Xmer):
					OutputFile.writelines('>%s_%s\n' % (Number,i))
					OutputFile.writelines(Line[i:i+Xmer]+"\n")

stop = timeit.default_timer()
print "Done;"
print "Time used: ", stop - start,    	