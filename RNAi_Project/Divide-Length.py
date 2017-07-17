import timeit;
start = timeit.default_timer()
import sys, optparse
import re
usage="python xx.py -i inputfile"
optParser = optparse.OptionParser(usage=usage)

optParser.add_option( "-i", "--input", type="string", dest="InputFile",
      default = "", help = "The file with gene ID that is to be annotated" )


(opts, args) = optParser.parse_args()

OutputFile = opts.InputFile.replace(".txt","-DivideLength.txt")

def main():
	with open (opts.InputFile,"r") as openInputFile, open (OutputFile,"w+") as openOutputFile:
		next(openInputFile)
		openOutputFile.write("ID\tInformation\n")
		for line in openInputFile:
			ElementList = line.strip("\n").split("\t")
			Length=float(ElementList[7])-float(ElementList[6])
			RegionPerLength= float(ElementList[1])/Length
			openOutputFile.write("%s\t%s\t%s\n" % ("\t".join(ElementList[0:2]),RegionPerLength, "\t".join(ElementList[2:])))

	stop = timeit.default_timer()
	print stop - start, "seconds. Done"
	




if __name__ == "__main__":
   main()
