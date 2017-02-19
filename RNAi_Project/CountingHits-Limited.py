import re;
import os;
import sys, optparse;
import timeit;
start = timeit.default_timer()

usage="python xx.py InputSamFile LimitedNumber"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
SamFile=infile[0]
#ReferenceFile=infile[1]
LimitedMulti=int(infile[1])
OutputFile1=SamFile.rstrip(".sam") + "_Transcriptlist-"+str(LimitedMulti)+".txt" 
OutputFile3=SamFile.rstrip(".sam") + "_GeneCountbyProbelist-"+str(LimitedMulti)+".txt"
#OutputFile2=SamFile.strip(".sam") + "_GeneCountbyReadlist.txt" 

try:
	with open (SamFile,"r") as openSamFile :
		print "SamFile OK"
except IOError:
	print "openning input file failed"


transCountDic={}
probeCountDic={}
#UniqueGeneCountDic={}
GeneName={}
UniqueCount=0
TotalCount=0

with open (SamFile,"r") as openSamFile :
	for samline in openSamFile:
		if "@" in samline:
			continue 
		content=samline.strip("\n").split("\t")
		probe=content[0]
		trans=content[2]
		#read=content[9]
		TotalCount+=1
		if int(content[19].split(":")[2])>LimitedMulti:
			continue
		UniqueCount+=1
		NameList=trans.split("|")
		GeneID=NameList[1]
		#print content[19]
		if GeneID not in GeneName:
			GeneName[GeneID]=NameList[5] + "\t" + NameList[7]
		else:
			if NameList[7] not in GeneName[GeneID]:
				GeneName[GeneID]=GeneName[GeneID]+";" + NameList[7]

		if trans not in transCountDic:
			transCountDic[trans] = 1
		else:
			transCountDic[trans] = transCountDic[trans]+1
		if GeneID not in probeCountDic:
			#UniqueGeneCountDic[GeneID] = []
			#UniqueGeneCountDic[GeneID].append(read)
			probeCountDic[GeneID]={}
			probeCountDic[GeneID][probe]=None
		else:
			#UniqueGeneCountDic[GeneID].append(read)
			probeCountDic[GeneID][probe]=None

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


with open(OutputFile3, "w+") as openOutputFile3:
	for gene in probeCountDic.keys():
		#print UniqueGeneCountDic[gene]
		#GeneCount=len(set(UniqueGeneCountDic[gene]))
		Genename=GeneName[gene]
		#openOutputFile2.write("%s\t%s\n" % (gene,GeneCount))
		probeCount=len((probeCountDic[gene]))
		#probeCount=len(set(probeCountDic[gene]))
		openOutputFile3.write("%s\t%s\t%s\n" % (gene,Genename,probeCount))



print "done part 2"
print "Unique Count:", UniqueCount,"\nTotal Conut:", TotalCount,"\nRatio:",float(UniqueCount)/float(TotalCount)
stop = timeit.default_timer()
print stop - start, "seconds"