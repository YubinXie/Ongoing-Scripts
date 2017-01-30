#!/usr/bin/python
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
Rstats = importr('stats')


usage="python xx.py ControlFile CaseFile "
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()

WholeReadsOutput=infile[1].strip("-counts.txt") + "-wholereads.txt"
SignificantReadsOutput=infile[1].strip("-counts.txt") + "-significantreads.txt"

WholeReadsFastaOutput=infile[1].strip("-counts.txt") + "-wholereads.fa"
SignificantReadsFastaOutput=infile[1].strip("-counts.txt") + "-significantreads.fa"
PadjustThreshold=0.05
FoldChangeThreshold=1
ControlDic = {}
TotalControlLineNumber=0
TotalCaseLineNumber=0
PvalueList=[]
OddsratioList=[]
with open(infile[0],"r") as ControlFile:
	for Line in ControlFile:
		ElementList = Line.strip("\n").split("\t")
		ControlDic[ElementList[0]] = int(ElementList[1])
		TotalControlLineNumber+=1

with open(infile[1],"r") as CaseFile:
	for Line in CaseFile:
		TotalCaseLineNumber+=1
		
with open(infile[1],"r") as CaseFile:
	for Line in CaseFile:
		ElementList = Line.strip("\n").split("\t")
		CaseCounts = ElementList[1]
		Reads = ElementList[0]
		if Reads not in ControlDic:
			ControlCounts = 0
		else:
			ControlCounts = ControlDic[Reads]
		Oddsratio, Pvalue = stats.fisher_exact([[ControlCounts,CaseCounts],[TotalControlLineNumber,TotalCaseLineNumber]], alternative="less")
		if Oddsratio==0:
			Oddsratio="inf"
		else:
			Oddsratio=1/Oddsratio
		PvalueList.append(Pvalue)
		OddsratioList.append(Oddsratio)

stop = timeit.default_timer()
print "Time used: ", stop - start,    #
print "\nCalculating P adjust"

P_adjustList = Rstats.p_adjust(FloatVector(PvalueList), method = 'bonferroni')
OutputLineNumbrt = 0
SignificantReadsNumber = 0

with open(infile[1],"r") as CaseFile, open (WholeReadsOutput,"w+") as OutputFile1, open (SignificantReadsOutput,"w+") as OutputFile2,open (WholeReadsFastaOutput,"w+") as OutputFile3,open (SignificantReadsFastaOutput,"w+") as OutputFile4 :
	OutputFile1.writelines('Reads\tCaseReadNumber\tControlReadNumber\tTotalCaseReadsNumber\tTotalControlLineNumber\tOddsRatio\tPvalue(fisher)\tP.adjust(bonferroni)\n')
	OutputFile2.writelines('Reads\tCaseReadNumber\tControlReadNumber\tTotalCaseReadsNumber\tTotalControlLineNumber\tOddsRatio\tPvalue(fisher)\tP.adjust(bonferroni)\n')
	for Line in CaseFile:
		ElementList = Line.strip("\n").split("\t")
		Reads = ElementList[0]
		CaseCounts = ElementList[1]
		if Reads not in ControlDic:
			ControlCounts = 0
		else:
			ControlCounts = ControlDic[Reads]
			FoldChange=float(CaseCounts)/float(ControlCounts)
		FastaName='>' + infile[1][0] + str(OutputLineNumbrt)
		OutputFile1.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (Reads,CaseCounts,ControlCounts,TotalCaseLineNumber,TotalControlLineNumber,OddsratioList[OutputLineNumbrt],PvalueList[OutputLineNumbrt],P_adjustList[OutputLineNumbrt]))
		OutputFile3.writelines('%s\n%s\n' % (FastaName, Reads))
		if P_adjustList[OutputLineNumbrt] <= PadjustThreshold:
			OutputFile2.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (Reads,CaseCounts,ControlCounts,TotalCaseLineNumber,TotalControlLineNumber,OddsratioList[OutputLineNumbrt],PvalueList[OutputLineNumbrt],P_adjustList[OutputLineNumbrt]))
			OutputFile4.writelines('%s\n%s\n' % (FastaName, Reads))
			SignificantReadsNumber+=1
		OutputLineNumbrt+=1


print "SignificantReadsNumber:",SignificantReadsNumber,"\nTotalCaseLineNumber: ",TotalCaseLineNumber, "\nSignificant rate:",folat(SignificantReadsNumber)/float(TotalCaseLineNumber)
stop = timeit.default_timer()
print "Time used: ", stop - start, "seconds"