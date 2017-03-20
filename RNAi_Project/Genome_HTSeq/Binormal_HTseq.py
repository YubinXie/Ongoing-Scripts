#!/usr/bin/python
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
Rstats = importr('stats')

usage="python xx.py ControlFile CaseFile Reference Pvalue"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

ControlFile = infile[0]
CaseFile = infile[1]
OutputFile1=CaseFile.strip(".txt").split("/")[-1] + "_Binormal.txt" 
Reference=infile[2]
Pvalue=float(infile[3])

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

with open (ControlFile,"r") as openControlFile:
	ControlDic= {}
	for line in openControlFile:
		ElementList=line.strip("\n").split("\t")
		ControlGene=ElementList[0]
		ControlGeneCounts=int(float(ElementList[1]))
		ControlDic[ControlGene]=ControlGeneCounts
stop = timeit.default_timer()
print stop - start, "seconds. Part 1 done"

with open (CaseFile,"r") as openCaseFile :
	PvalueList=[]
	for line in openCaseFile:
		ElementList=line.strip("\n").split("\t")
		Gene=ElementList[0]
		if "ENSG" not in Gene:
			continue
		CaseGeneCounts=int(float(ElementList[1]))
		if CaseGeneCounts == 0:
			continue
		if Gene not in ControlDic:
			ControlGeneCounts=0
		else:
			ControlGeneCounts=int(ControlDic[Gene])
		if CaseGeneCounts > ControlGeneCounts:
			print Gene,"CaseGeneCounts > ControlGeneCounts"
			BinormalPvalue=1
		else:
			BinormalPvalue=stats.binom_test(CaseGeneCounts,ControlGeneCounts,Pvalue)
		PvalueList.append(BinormalPvalue)
		#print CaseGeneCounts,ControlGeneCounts,Pvalue,BinormalPvalue

P_adjustList = Rstats.p_adjust(FloatVector(PvalueList), method = 'fdr')

stop = timeit.default_timer()
print stop - start, "seconds. Part 2 done"

with open (CaseFile,"r") as openCaseFile, open (OutputFile1,"w+") as openOutputFile :
	openOutputFile.write("GeneID\tCaseCounts\tControlCounts\tPro.\tPvalue\tP.adjust\n")
	i=0
	for line in openCaseFile:
		ElementList=line.strip("\n").split("\t")
		Gene=ElementList[0]
		if "ENSG" not in Gene:
			continue
		CaseGeneCounts=int(float(ElementList[1]))
		if CaseGeneCounts == 0:
			continue
		if Gene not in ControlDic:
			ControlGeneCounts=0
		else:
			ControlGeneCounts=int(ControlDic[Gene])
		BinormalPvalue=PvalueList[i]
		Padjust=P_adjustList[i]
		if Gene in ReferenceDic:
			Information=ReferenceDic[Gene].strip("\n").replace('"',"").replace('gene_name ',"").replace('gene_type ',"")
		else:
			Information="NA"
			print "no information"
		openOutputFile.write("%s\t%s\t%s\t%s\t%e\t%e\t%s\n" % (Gene,CaseGeneCounts,ControlGeneCounts,Pvalue,BinormalPvalue,Padjust,Information))
		i+=1

stop = timeit.default_timer()
print stop - start, "seconds. Part 3 done"