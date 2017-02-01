#!/usr/bin/python
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import numpy as np
Rstats = importr('stats')
from fisher import pvalue

usage="python xx.py ControlFile CaseFile ControlReadsTotalNumber CaseReadsTotalNumber"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

TotalControlLineNumber=int(infile[2])
TotalCaseLineNumber= int(infile[3])
TotalCaseUReadNumber=0
WholeReadsOutput=infile[1].strip("-counts.txt") + "-wholereads.txt"
Significant_twosideReadsOutput=infile[1].strip("-counts.txt") + "-twosidesignificantreads.txt"
Significant_rightsideReadsOutput=infile[1].strip("-counts.txt") + "-rightsidesignificantreads.txt"


WholeReadsFastaOutput=infile[1].strip("-counts.txt") + "-wholereads.fa"
Significant_twosideReadsFastaOutput=infile[1].strip("-counts.txt") + "-twosidesignificantreads.fa"
Significant_rightsideReadsFastaOutput=infile[1].strip("-counts.txt") + "-rightsidesignificantreads.fa"

PadjustThreshold=0.05
FoldChangeThreshold=1
ControlDic = {}
PvalueTwosideList=[]
PvalueRightsideList=[]
OddsratioList=[]
OddDic={}
with open(infile[0],"r") as ControlFile:
	for Line in ControlFile:
		ElementList = Line.strip("\n").split("\t")
		ControlDic[ElementList[0]] = int(ElementList[1])

with open(infile[1],"r") as CaseFile:
	for Line in CaseFile:
		TotalCaseUReadNumber+=1
		
with open(infile[1],"r") as CaseFile:
	for Line in CaseFile:
		ElementList = Line.strip("\n").split("\t")
		CaseCounts = int (ElementList[1])
		Reads = ElementList[0]
		if Reads not in ControlDic:
			ControlCounts = 0
		else:
			ControlCounts = ControlDic[Reads]
		#Oddsratio, Pvalue = stats.fisher_exact([[ControlCounts,CaseCounts],[TotalControlLineNumber,TotalCaseLineNumber]])
		P=pvalue(ControlCounts,CaseCounts,TotalControlLineNumber,TotalCaseLineNumber)
		Pvalue_twoside = P.two_tail
		Pvalue_rightside = P.left_tail
		#print TotalCaseLineNumber, TotalControlLineNumber + TotalCaseUReadNumber,ControlCounts+1
		FoldChange=(float(CaseCounts))*(float((TotalControlLineNumber + TotalCaseUReadNumber)))/(float((ControlCounts+1))*float(TotalCaseLineNumber))
		PvalueTwosideList.append(Pvalue_twoside)
		PvalueRightsideList.append(Pvalue_rightside)
		OddDic[Reads]=FoldChange

stop = timeit.default_timer()
print "Time used: ", stop - start,    #
print "\nCalculating P adjust"

Ptwoside_adjustList = Rstats.p_adjust(FloatVector(PvalueTwosideList), method = 'bonferroni')
Prightside_adjustList = Rstats.p_adjust(FloatVector(PvalueRightsideList), method = 'bonferroni')
OutputLineNumbrt = 0
twosideSignificantReadsNumber = 0
rightsideSignificantReadsNumber = 0

with open(infile[1],"r") as CaseFile, open (WholeReadsOutput,"w+") as OutputFile1, open (Significant_twosideReadsOutput,"w+") as OutputFile2,open (WholeReadsFastaOutput,"w+") as OutputFile3,open (Significant_twosideReadsFastaOutput,"w+") as OutputFile4, open (Significant_rightsideReadsOutput,"w+") as OutputFile5, open (Significant_rightsideReadsFastaOutput,"w+") as OutputFile6 :
	OutputFile1.writelines('Reads\tCaseReadNumber\tControlReadNumber\tTotalCaseReadsNumber\tTotalControlLineNumber\tFC\tPtwosidevalue(fisher)\tPtwoside.adjust(bonferroni)\tPrightsidevalue(fisher)\tPrightside.adjust(bonferroni)\n')
	OutputFile2.writelines('Reads\tCaseReadNumber\tControlReadNumber\tTotalCaseReadsNumber\tTotalControlLineNumber\tFC\tPtwosidevalue(fisher)\tPtwoside.adjust(bonferroni)\n')
	OutputFile5.writelines('Reads\tCaseReadNumber\tControlReadNumber\tTotalCaseReadsNumber\tTotalControlLineNumber\tFC\tPrightsidevalue(fisher)\tPrightside.adjust(bonferroni)\n')
	for Line in CaseFile:
		ElementList = Line.strip("\n").split("\t")
		Reads = ElementList[0]
		CaseCounts = ElementList[1]
		if Reads not in ControlDic:
			ControlCounts = 0
		else:
			ControlCounts = ControlDic[Reads]
		FastaName='>' + infile[1][0] + str(OutputLineNumbrt)
		OutputFile1.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (Reads,CaseCounts,ControlCounts,TotalCaseLineNumber,TotalControlLineNumber,OddDic[Reads],PvalueTwosideList[OutputLineNumbrt],Ptwoside_adjustList[OutputLineNumbrt],PvalueRightsideList[OutputLineNumbrt],Prightside_adjustList[OutputLineNumbrt]))
		OutputFile3.writelines('%s\n%s\n' % (FastaName, Reads))
		if (Ptwoside_adjustList[OutputLineNumbrt] < PadjustThreshold) & (OddDic[Reads] > FoldChangeThreshold):
			OutputFile2.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (Reads,CaseCounts,ControlCounts,TotalCaseLineNumber,TotalControlLineNumber,OddDic[Reads],PvalueTwosideList[OutputLineNumbrt],Ptwoside_adjustList[OutputLineNumbrt]))
			OutputFile4.writelines('%s\n%s\n' % (FastaName, Reads))
			twosideSignificantReadsNumber+=1
		if (Prightside_adjustList[OutputLineNumbrt] < PadjustThreshold) & (OddDic[Reads] > FoldChangeThreshold):
			OutputFile5.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (Reads,CaseCounts,ControlCounts,TotalCaseLineNumber,TotalControlLineNumber,OddDic[Reads],PvalueRightsideList[OutputLineNumbrt],Prightside_adjustList[OutputLineNumbrt]))
			OutputFile6.writelines('%s\n%s\n' % (FastaName, Reads))
			rightsideSignificantReadsNumber+=1
		OutputLineNumbrt+=1


print "twosideSignificantReadsNumber:",twosideSignificantReadsNumber,"\nrightsideSignificantReadsNumber:",rightsideSignificantReadsNumber,"\nTotalCaseLineNumber: ",TotalCaseLineNumber, "\ntwosideSignificant rate:",float(twosideSignificantReadsNumber)/float(TotalCaseLineNumber), "\nrightsideSignificant rate:",float(rightsideSignificantReadsNumber)/float(TotalCaseLineNumber)
stop = timeit.default_timer()
print "Time used: ", stop - start, "seconds"