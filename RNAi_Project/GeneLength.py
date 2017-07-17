import timeit;
start = timeit.default_timer()
import sys, optparse
import re
usage="python xx.py -i inputfile"
optParser = optparse.OptionParser(usage=usage)

optParser.add_option( "-i", "--input", type="string", dest="InputFile",
      default = "", help = "The file with gene ID that is to be annotated" )


(opts, args) = optParser.parse_args()

OutputFile = opts.InputFile.replace(".gtf","-ProteinCodingGeneLength.txt")

def main():
	with open (opts.InputFile,"r") as openInputFile, open (OutputFile,"w+") as openOutputFile:
		for line in openInputFile:
			if "#" in line:
				continue
			ElementList = line.strip("\n").split("\t")
			Property = ElementList[2]   #Gene or not
			Attribute  =  ElementList[]       # Protein coding or others
			Length=int(ElementList[]) - int(ElementList[]) 
			GeneName= ElementList[]
			GeneID= ElementList[8].split("\"")[]
			openOutputFile.write("%s\t%s\t%s\n" % (GeneID, GeneName,Length))


	

if __name__ == "__main__":
   main()
   stop = timeit.default_timer()
   print stop - start, "seconds. Done"
