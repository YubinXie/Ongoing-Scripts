import sys, optparse
import timeit;
import re
start = timeit.default_timer()

usage="python xx.py XXX.sam"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

InputFile=infile[0]
LimitedMulti=infile[1]
OutputFile=InputFile.rstrip(".sam")+"-LimitMultiHit-"+LimitedMulti+".sam"

ProbeDic={}
TotalProbeDic={}

with open (InputFile,"r") as OpenInputFile, open (OutputFile,"w+") as OpenOutputFile :
	for line in OpenInputFile:
		if "@" in line:
			continue
		ElementList=line.rstrip("\n").split("\t")
		
		MultiHit=re.search('NH:i:(?P<h1>.+?)\t',line)
		if MultiHit:
			MultiHitNumber=MultiHit.group("h1")
		else:
			#m  print line
			MultiHitNumber=1

		TotalProbeDic[ElementList[0]]=None
		if int(MultiHitNumber)> int(LimitedMulti) :
			continue
		#print MultiHitNumber
		OpenOutputFile.write("%s\n" % ("\t").join(ElementList[0:11]))
		ProbeDic[ElementList[0]]=None

stop = timeit.default_timer()
print stop - start, "seconds. ProbeNumber:",len(ProbeDic),len(TotalProbeDic)