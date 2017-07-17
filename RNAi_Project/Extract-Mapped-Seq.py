import timeit;
start = timeit.default_timer()
import sys, optparse
import re
import numpy

usage="python xx.py -i SamInputFile -r 19merFastaReference -w WeightF ile"
optParser = optparse.OptionParser(usage=usage)

optParser.add_option( "-i", "--input", type="string", dest="InputFile",
      default = "", help = "" )
optParser.add_option( "-r", "--reference", type="string", dest="Reference",
      default = "", help = "" )
optParser.add_option( "-w", "--weightfile", type="string", dest="WeightFile",
      default = "", help = "" )



(opts, args) = optParser.parse_args()


OutputFile = opts.InputFile.replace(".sam","-MappedSequence.txt")
ReadIDDic={}
ReadWeightDic={}
OutputDic={}

with open(opts.WeightFile,"r") as OpenWeightFile:
	next(OpenWeightFile)
	for line in OpenWeightFile:
		ElementList=line.strip("\n").split("\t")
		#print ElementList
		Read=ElementList[0]
		PAdjust=float(ElementList[9])
		if PAdjust<=0.05:
			Weight=numpy.log(float(ElementList[5]))
		else:
			Weight=0
		ReadWeightDic[Read]=Weight


with open (opts.Reference,"r") as OpenReference:
	for line in OpenReference:
		if ">" in line:
			ReadID=line.lstrip(">").rstrip("\n")
			continue
		ReadIDDic[ReadID]=line.strip("\n")



with open (opts.InputFile,"r") as OpenSamFile, open (OutputFile,"w+") as OpenOutputFile:
	for line in OpenSamFile:
		if "@" in line:
			continue
		if "NH:i:1\n" not in line:
			continue
		#print "yes"
		ElementList = line.split("\t")
		SeqIDinSam = ElementList[0]
		#print SeqIDinSam
		ReadIDinSam = SeqIDinSam.split("_")[0]
		#print ReadIDinSam
		Mismatch = ElementList[16].split(":")[2]
		#print Mismatch
		ReadinSam = ReadIDDic[ReadIDinSam]
		#print ReadinSam
		ReadWeight = ReadWeightDic[ReadinSam]
		#print SeqIDinSam,ReadIDinSam,ReadinSam,ReadWeight,Mismatch
		OpenOutputFile.writelines("%s\t%s\t%s\t%s\t%s\n" % (SeqIDinSam,ReadIDinSam,ReadinSam,ReadWeight,Mismatch))
		




















