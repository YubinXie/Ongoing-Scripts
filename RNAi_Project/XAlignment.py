import sys, optparse
import timeit;
import re
start = timeit.default_timer()

usage="python xx.py XXX.sam "
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

InputFile=infile[0]
OutputFile=InputFile.replace(".sam","UniqueAlignmentOnly.sam")


with open (InputFile,"r") as OpenInputFile, open (OutputFile,"w+") as OpenOutputFile :
	for line in OpenInputFile:
		if "@" in line:
			continue
		if "NH:i:1\n" in line:
			OpenOutputFile.write(line)
		#if "NH:i:2\t" in line:
			#OpenOutputFile.write(line)


stop = timeit.default_timer()
print stop - start, "seconds."