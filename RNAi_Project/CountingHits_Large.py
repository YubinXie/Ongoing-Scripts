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
OutputFile1=SamFile.rstrip(".sam") + "_Transcriptlist.txt" 
OutputFile3=SamFile.rstrip(".sam") + "_GeneCountbyProbelist.txt"
#OutputFile2=SamFile.strip(".sam") + "_GeneCountbyReadlist.txt" 

try:
	with open (SamFile,"r") as openSamFile :
		print "SamFile OK"
except IOError:
	print "openning input file failed"



#UniqueGeneCountDic={}
transCountDic={}
probeCountDic={}
GeneName={}

with open (SamFile,"r") as openSamFile :
	for samline in openSamFile:
		transDic={}
		probeDic={}
		GeneName={}
		if "@" in samline:
			continue 
		content=samline.strip("\n").split("\t")
		trans=content[2]
		NameList=trans.split("|")
		GeneID=NameList[1]

		if trans not in transCountDic:
			transCountDic[trans] = 1
		else:
			transCountDic[trans] = transCountDic[trans]+1
				
		print "Trans Done\n"

		if GeneID not in probeCountDic:
			GeneName[GeneID]=NameList[5] + "\t" + NameList[7]
			probelist =[]
			with open (SamFile,"r") as openSamFile3 :
				for samline in openSamFile3:
					if "@" in samline:
						continue 
					content=samline.strip("\n").split("\t")
					subGeneID=NameList[1]
					subprobe=content[0]
					if subGeneID == GeneID:
						probelist.append(subprobe)
				probeCountDic[GeneID]=len(probelist)


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
		probeCount=probeCountDic[gene]
		openOutputFile3.write("%s\t%s\t%s\n" % (gene,Genename,probeCount))



print "done part 2"
stop = timeit.default_timer()
print stop - start, "seconds"