#!/usr/bin/python
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse

usage="python xx.py ControlFile CaseFile Pvalue"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

ControlFile = infile[0]
CaseFile = infile[1]
OutputFile1=CaseFile.strip(".txt") + "_Binormal.txt" 
Pvalue=infile[2]

with open (ControlFile,"r") as openControlFile:
ControlDic= {}
	for line in openControlFile:
		ElementList=line.strip("\n").split("\t")
		ControlGene=ElementList[0]
		ControlGeneCounts=ElementList[1]
		ControlDic[ControlGene]=ControlGeneCounts

with open (CaseFile,"r") as openCaseFile:
	for line in openCaseFile:
		ElementList=line.strip("\n").split("\t")
		Gene=ElementList[0]
		CaseGeneCounts=ElementList[1]
		if Gene not in ControlDic:
			ControlGeneCounts=0
		else:
			ControlGeneCounts=ControlDic[Gene]
		BinormalPvalue=scipy.stats.binom_test(CaseGeneCounts,ControlGeneCounts,Pvalue,alternative="greater")