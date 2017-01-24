import re;
import os;
import sys, optparse;
import timeit;
start = timeit.default_timer()

usage="python xx.py InputSamFile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
SamFile=infile[0]
#ReferenceFile=infile[1]
OutputFile1=SamFile.strip(".sam") + "_Transcriptlist.txt" 
OutputFile3=SamFile.strip(".sam") + "_GeneCountbyProbelist.txt"
OutputFile2=SamFile.strip(".sam") + "_GeneCountbyReadlist.txt" 

try:
	with open (SamFile,"r") as openSamFile :
		print "SamFile OK"
except IOError:
	print "openning input file failed"


transCountDic={}
probeCountDic={}
UniqueGeneCountDic={}
GeneName={}

with open (SamFile,"r") as openSamFile :
	for samline in openSamFile:
		if "@" in samline:
			continue 
		content=samline.strip("\n").split("\t")
		probe=content[0]
		trans=content[2]
		read=content[9]
		NameList=trans.split("|")
		GeneID=NameList[1]
		GeneName[GeneID]=NameList[5] + NameList[7]

		if trans not in transCountDic:
			transCountDic[trans] = 1
		else:
			transCountDic[trans] = transCountDic[trans]+1
		if GeneID not in UniqueGeneCountDic:
			UniqueGeneCountDic[GeneID] = []
			UniqueGeneCountDic[GeneID].append(read)
			probeCountDic[GeneID]=[]
			probeCountDic[GeneID].append(probe)
		else:
			UniqueGeneCountDic[GeneID].append(read)
			probeCountDic[GeneID].append(probe)

print "done part 1"
stop = timeit.default_timer()
print stop - start, "seconds"
#print probelist



##################4
with open(OutputFile1,"w+") as openOutputFile1:
	for trans in transCountDic.keys():
		SamGeneHits=(transCountDic[trans])
		trans = trans.replace('|','\t')
		openOutputFile1.write("%s%s\n" % (trans,SamGeneHits))


with open(OutputFile2, "w+") as openOutputFile2, open(OutputFile3, "w+") as openOutputFile3:
	for gene in UniqueGeneCountDic.keys():
		#print UniqueGeneCountDic[gene]
		GeneCount=len(set(UniqueGeneCountDic[gene]))
		Genename=GeneName[gene]
		openOutputFile2.write("%s\t%s\n" % (gene,GeneCount))
		probeCount=len(set(probeCountDic[gene]))
		openOutputFile3.write("%s\t%s\t%s\n" % (gene,GeneCount,probeCount))



print "done part 2"
stop = timeit.default_timer()
print stop - start, "seconds"