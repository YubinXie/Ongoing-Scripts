import sys, optparse


usage="python xx.py InputFile1"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

InputFile1=infile[0]

with open (InputFile1,"r") as openInputFile1:
	summ=0
	for line in openInputFile1:
		line=line.strip("\n").split("\t")
		count=int(line[1])
		summ=summ+count
	print "Total count:",summ