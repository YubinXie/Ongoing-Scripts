import re;
import os;
import sys, optparse;
import timeit;
start = timeit.default_timer()

usage="python xx.py InputSamFile Reference"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
SamFile=infile[0]
referencefile=infile[1]
OutputFile1="genelist.txt" 
OutputFile2="probelist.txt"
openOutputFile1=open(OutputFile1,"w+")
openOutputFile2=open(OutputFile2,"w+")
try:
	with open (SamFile,"r") as openSamFile :
		print "SamFile OK"
except IOError:
	print "openning input file failed"

try:
	with open (referencefile,"r") as openreferencefile:
		print "reference file OK"
except IOError:
	print "openning reference file failed"


###################1
D={}
with open (referencefile,"r") as openreferencefile:
	for lines in openreferencefile:
		content=re.search('>(?P<h1>.+?)\n',lines)
		if(content):
			seqname=content.group("h1")
		else:
			seqcontent=lines.rstrip("\n")
			D[seqname]=len(seqcontent)
			#print seqname,seqcontent, D[seqname]
print "done part 1"

##################2
probelist=[]
probeCountDic={}
genelist=[]
geneCountDic={}
with open (SamFile,"r") as openSamFile :
	for samline in openSamFile:
		content=samline.split("\t")
		probe=content[0]
		gene=content[2]
		if probe not in probelist:
			probelist.append(probe)
			probeCountDic[probe]=1
		else:
			probeCountDic[probe]=probeCountDic[probe]+1
		if gene not in genelist:
			genelist.append(gene)
			geneCountDic[gene]=1
		else:
			geneCountDic[gene]=geneCountDic[gene]+1

print "done part 2"
#print probelist
###################3
for probe in probelist:
	openOutputFile2.write("%s\t%s\n" % (probe,probeCountDic[probe]))
print "done part 3"

##################4
for gene in genelist:
	#print gene,"\n",geneCountDic[gene],"\n",D[gene],"\n"
	ratio=float(geneCountDic[gene])/float(D[gene])
	#print ratio
	openOutputFile1.write("%s\t%s\t%s\t%.5f\n" % (gene,D[gene],geneCountDic[gene],ratio))
print "done part 4"
stop = timeit.default_timer()
print stop - start