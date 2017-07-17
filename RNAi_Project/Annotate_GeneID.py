import timeit;
start = timeit.default_timer()
import sys, optparse
usage="python xx.py -i inputfile -r reference"
optParser = optparse.OptionParser(usage=usage)

optParser.add_option( "-i", "--input", type="string", dest="InputFile",
      default = "", help = "The file with gene ID that is to be annotated" )

optParser.add_option( "-r", "--reference", type="string", dest="Reference",
      default = "", help = "The file with annotation" )

(opts, args)= optParser.parse_args()
InputFile=opts.InputFile
Reference=opts.Reference
OutputFile = InputFile.replace(".txt","_annotated.txt")

with open(Reference,"r") as openReference:
	ReferenceDic={}
	for line in openReference:
		ElementList=line.strip("\n").split("\t")
		Output=line.replace(";","\t")
		if len(ElementList)<8:
			continue
		GeneID = ElementList[8].split('"')[1]
		if ElementList[2]=="gene":
			ReferenceDic[GeneID]=Output


with open (InputFile,"r") as openInputFile, open (OutputFile,"w+") as openOutputFile :
	Header=0
	i=0
	for line in openInputFile:
		ElementList=line.strip("\n").split("\t")
		Gene=ElementList[0]
		if "ENS" not in Gene:
			
			Header+=1
			if Header>=2:
				continue
				print "No Gene ID found"
			else: 
				print "This file contains head line"
			openOutputFile.writelines(line)
			continue

		GeneCounts=int(float(ElementList[1]))
		if GeneCounts == 0:
			continue
		if Gene in ReferenceDic:
			Information=ReferenceDic[Gene].strip("\n").replace('"',"").replace('gene_name ',"").replace('gene_type ',"")
		else:
			Information="NA"
			print "no information"
		openOutputFile.writelines("%s\t%s\n" % (line.strip("\n"),Information))
		i+=1

stop = timeit.default_timer()
print stop - start, "seconds. Done"