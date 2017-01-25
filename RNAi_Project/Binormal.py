#!/usr/bin/python
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
Rstats = importr('stats')

usage="python xx.py ControlFile CaseFile Pvalue"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

ControlFile = infile[0]
CaseFile = infile[1]
OutputFile1=CaseFile.strip(".txt").split("/")[-1] + "_Binormal.csv" 
Pvalue=float(infile[2])

with open (ControlFile,"r") as openControlFile:
	ControlDic= {}
	for line in openControlFile:
		ElementList=line.strip("\n").split("\t")
		ControlGene=ElementList[0]
		ControlGeneCounts=ElementList[3]
		ControlDic[ControlGene]=ControlGeneCounts
stop = timeit.default_timer()
print stop - start, "seconds. Part 1 done"

with open (CaseFile,"r") as openCaseFile :
	PvalueList=[]
	for line in openCaseFile:
		ElementList=line.strip("\n").split("\t")
		Gene=ElementList[0]
		CaseGeneCounts=int(ElementList[3])
		if Gene not in ControlDic:
			ControlGeneCounts=0
		else:
			ControlGeneCounts=int(ControlDic[Gene])
		if CaseGeneCounts > ControlGeneCounts:
			print "CaseGeneCounts > ControlGeneCounts"
		BinormalPvalue=stats.binom_test(CaseGeneCounts,ControlGeneCounts,Pvalue)
		PvalueList.append(BinormalPvalue)


P_adjustList = Rstats.p_adjust(FloatVector(PvalueList), method = 'fdr')

stop = timeit.default_timer()
print stop - start, "seconds. Part 2 done"

with open (CaseFile,"r") as openCaseFile, open (OutputFile1,"w+") as openOutputFile :
	openOutputFile.write("GeneID\tGeneName\tGeneType\tCaseCounts\tControlCounts\tPro.\tPvalue\tP.adjust\n")
	i=0
	for line in openCaseFile:
		ElementList=line.strip("\n").split("\t")
		Gene=ElementList[0]
		GeneName=ElementList[1]
		GeneType=ElementList[2]
		CaseGeneCounts=int(ElementList[3])
		if Gene not in ControlDic:
			ControlGeneCounts=0
		else:
			ControlGeneCounts=int(ControlDic[Gene])
		BinormalPvalue=PvalueList[i]
		Padjust=P_adjustList[i]
		openOutputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%e\t%e\n" % (Gene,GeneName,GeneType,CaseGeneCounts,ControlGeneCounts,Pvalue,BinormalPvalue,Padjust))
		i+=1

stop = timeit.default_timer()
print stop - start, "seconds. Part 3 done"