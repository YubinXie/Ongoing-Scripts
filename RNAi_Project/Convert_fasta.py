import sys, optparse
import timeit;
start = timeit.default_timer()

usage="python xx.py InputFile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
InputFile=infile[0]
OutputFile=InputFile.replace(".fa","-renamed.fa")

with open (InputFile,"r") as OpenInputFile, open (OutputFile,"w+") as OpenOutputFile:
	for line in OpenInputFile:
		if ">" in line:
			ElementList=line.strip("\n").split(" ")
			#print ElementList[1]
			OpenOutputFile.write(">%s %s" % (ElementList[1],line.replace(ElementList[0],"")))
		else:
			OpenOutputFile.write(line)