import re;
import os;
import sys, optparse;
import timeit;
start = timeit.default_timer()

usage="python xx.py InputSamFile Reference"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
SamFile=infile[0]
ReferenceFile=infile[1]
OutputFile1=SamFile.strip(".sam") + "_Transcriptlist.txt" 
OutputFile2=SamFile.strip(".sam") + "_Probelist.txt"
OutputFile3=SamFile.strip(".sam") + "_Genelist.txt" 

try:
	with open (SamFile,"r") as openSamFile :
		print "SamFile OK"
except IOError:
	print "openning input file failed"

try:
	with open (ReferenceFile,"r") as openReferenceFile:
		print "reference file OK"
except IOError:
	print "openning reference file failed"


###################1
D={}

with open (ReferenceFile,"r") as openReferenceFile:
	for lines in openReferenceFile:
		if ">" in lines:
			seqname=lines.lstrip(">").rstrip("\n")
			#print seqname
		else:
			seqcontent=lines.rstrip("\n")
			D[seqname]=len(seqcontent)
			#print seqname,seqcontent, D[seqname]
print "done part 1"
stop = timeit.default_timer()
print stop - start, "seconds"

##################2
probelist=[]
probeCountDic={}
genelist=[]
geneCountDic={}

with open (SamFile,"r") as openSamFile :
	for samline in openSamFile:
		if "@" in samline:
			continue 
		content=samline.strip("\n").split("\t")
		probe=content[0]
		gene=content[2]
		if probe not in probeCountDic:
			probeCountDic[probe]=1
			#print probe
		else:
			probeCountDic[probe]=probeCountDic[probe]+1
		if gene not in geneCountDic:
			geneCountDic[gene]=1
		else:
			geneCountDic[gene]=geneCountDic[gene]+1

print "done part 2"
stop = timeit.default_timer()
print stop - start, "seconds"
#print probelist


###################3
with open(OutputFile2,"w+") as openOutputFile2:
	for probe in probeCountDic.keys():
		openOutputFile2.write("%s\t%s\n" % (probe,probeCountDic[probe]))

print "done part 3"
stop = timeit.default_timer()
print stop - start, "seconds"


UniqueGeneCountDic={}

##################4
with open(OutputFile1,"w+") as openOutputFile1:
	for gene in geneCountDic.keys():
		ReferenceLength=(D[gene])
		SamGeneHits=(geneCountDic[gene])
		#print gene,"\n",geneCountDic[gene],"\n",D[gene],"\n"
		ratio=float(SamGeneHits)/float(ReferenceLength)
		gene=gene.replace('|','\t')
		openOutputFile1.write("%s%s\t%s\t%.5f\n" % (gene,ReferenceLength,SamGeneHits,ratio))
		GeneID=gene.split("\t")[1]
		if GeneID not in UniqueGeneCountDic:
			UniqueGeneCountDic[GeneID]=SamGeneHits
		else:
			UniqueGeneCountDic[GeneID]=max(UniqueGeneCountDic[GeneID],SamGeneHits)

with open(OutputFile3, "w+") as openOutputFile3:
	for gene in UniqueGeneCountDic.keys():
		openOutputFile3.write("%s\t%s\n" % (gene,UniqueGeneCountDic[gene]))



print "done part 4"
stop = timeit.default_timer()
print stop - start, "seconds"