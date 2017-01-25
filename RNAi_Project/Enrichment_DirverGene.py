#####################
#To analize the overlap of two dataset, driver gene and TC results
#v4.0;with hypergeometric test. with enrichment fold
#Yubin Xie 11.16.2016
#####################
from xlrd import open_workbook
import xlsxwriter
import sys
import scipy.stats as stats
import sys, optparse
###################Input ##################
usage="python xx.py ControlFile CaseFile Pvalue"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
ResultFilename=""

NumberofReferenceSheetList=[0,1,2,3] #adjustable
NumberofReferenceColList=[1,1,1,1] #adjustable
NumberofResultCol=2 #adjustable DrugV=13,MEF=9
NumberofResultPvalueCol=7
NumberofResultGenetypeCol=3

pvalue_shresholdlist=[2.6e-20,2.25e-10,2e-7,2e-6,5e-6,1e-5,2e-5,5e-5,1e-4,5e-4,1e-3,5e-3,1e-2,2e-2,3e-2,5e-2]
Qvalue_shresholdlist=[6.14E-16,5.37e-6,0.005,0.05,0.1189,0.2368,0.4752,1,1,1,1,1,1,1,1,1]

ReferenceList=["drivergene.xlsx","drivergene.xlsx","drivergene.xlsx","drivergene.xlsx"]
SheetNameeList=["AllGene","KnowGene","Newgene","Melanoma"]
workbook=xlsxwriter.Workbook("SummaryofOverlap_TC_drivergene_1-24.xlsx")
ResultSheetNameeList=["HumanDrugV15mer"]
Population=[20000,20000,20000,20000]
bold = workbook.add_format()
red=workbook.add_format()
yellow=workbook.add_format()
black=workbook.add_format()
bold.set_bold()
red.set_font_color('red')
yellow.set_font_color('yellow')
black.set_font_color('black')
#################################################
for ResultUnit in range(2):
	NumberofResultSheet=ResultUnit
	worksheet=workbook.add_worksheet(ResultSheetNameeList[ResultUnit])
	worksheet.write(0, 0, "Pvalue",bold)
	worksheet.write(0, 2, "TotalGeneinTC",bold)
	worksheet.write(0, 1, "Qvalue",bold)
	ReferenceGeneNameNumberList=[]
	for Unit in range(len(ReferenceList)):
	####################Initial######################
		row=1
		col=5*Unit+3
		
		NumberofReferenceSheet=NumberofReferenceSheetList[Unit]
		NumberofReferenceCol=NumberofReferenceColList[Unit]
		SheetNamee=SheetNameeList[Unit]
		ReferenceFilename=ReferenceList[Unit]
		ReferenceFile=open_workbook(ReferenceFilename)
		ResultFile=open_workbook(ResultFilename)

		ReferenceSheetName=ReferenceFile.sheet_names()

		#print ReferenceSheetName[NumberofReferenceSheet]
		ReferenceData=ReferenceFile.sheet_by_name(ReferenceSheetName[NumberofReferenceSheet])
		ReferenceGeneName=ReferenceData.col(NumberofReferenceCol)
		ReferenceGeneNameNew=[]
		for x in ReferenceGeneName:
			if str(x.value) not in ReferenceGeneNameNew:
				ReferenceGeneNameNew.append(str(x.value))
		#print "Name of ReferenceCol =" ,ReferenceGeneNameNew[0],"\nNumberofreferenceGene=",len(ReferenceGeneNameNew)-1
		ReferenceGeneNameNew=ReferenceGeneNameNew[1:]

		ReferenceGeneNameNumberList.append(len(ReferenceGeneNameNew))

		ResultSheetName=ResultFile.sheet_names()
		print ResultSheetName[NumberofResultSheet]
		ResultData=ResultFile.sheet_by_name(ResultSheetName[NumberofResultSheet])
		ResultGeneName=ResultData.col(NumberofResultCol)
		ResultPvalue=ResultData.col(NumberofResultPvalueCol)
		ResultGenetype=ResultData.col(NumberofResultGenetypeCol)
		PvalueCol=str(ResultPvalue[0].value)
		ResultGenetypeCol=str(ResultGenetype[0].value)
		ResultGeneNameStr=[]
		ResultGenetypeStr=[]
		ResultPvalueStr=[]
		for x in ResultGeneName:
			ResultGeneNameStr.append(str(x.value))

		for x in ResultGenetype:
			ResultGenetypeStr.append(str(x.value))

		ResultPvalue=ResultPvalue[1:]
		ResultGeneNameStr=ResultGeneNameStr[1:]
		ResultGenetypeStr=ResultGenetypeStr[1:]
		for x in ResultPvalue:
			ResultPvalueStr.append(float(x.value))
		#print len(ResultPvalueStr)
	####################################################################


		#REAL LOOP########################
		FinalOverlapGeneNumberList=[]
		FinalOverlapGeneNameList=[]
		TotalGeneNumberList=[]
		for pvalue_shreshold in pvalue_shresholdlist:
			ResultGeneNameSelected=[]
			#print PvalueCol,pvalue_shreshold,"\t",ResultGenetypeCol,"protein_coding"
			for resultgene in range(1,len(ResultGeneName)-1):
				#print ResultGenetypeStr[x],"\n",ResultPvalueStr[x]
				if ResultGenetypeStr[resultgene] == "protein_coding" and ResultPvalueStr[resultgene] < pvalue_shreshold:
					ResultGeneNameSelected.append(ResultGeneNameStr[resultgene])
			#print "Name of ResultCol =" ,str(ResultGeneName[0].value),"\nNumberofResultGene=",len(ResultGeneNameSelected)

			OverlapNumber=0
			OverlapGene=[]
			FinalOverlapGene=[]
			for SelectedGene in ResultGeneNameSelected:
				for y in ReferenceGeneNameNew:
					if SelectedGene==y:
						OverlapNumber=OverlapNumber+1
						OverlapGene.append(SelectedGene)
			for overlapgene in OverlapGene:
				if overlapgene not in FinalOverlapGene:
					FinalOverlapGene.append(overlapgene)		
			FinalOverlapGeneNumberList.append(len(FinalOverlapGene))
			FinalOverlapGeneNameList.append(FinalOverlapGene)
			TotalGeneNumberList.append(len(ResultGeneNameSelected))
			#print "OverlapNumber=",len(FinalOverlapGene),"\n","OverlapGene=",FinalOverlapGene
		#print ResultGeneNameNew, "\n",ReferenceGeneNameNew
			#print TotalGeneNumberList

###########OUTPUT##########
		worksheet.write(0, col, SheetNamee+"("+str(len(ReferenceGeneNameNew))+"):",bold)
		worksheet.write(0, col+1, "OverlapNumber with "+SheetNamee,bold)
		worksheet.write(0, col+2, "OverlapGene with "+SheetNamee,bold)
		worksheet.write(0, col+3, "p value of hypergeometric with "+SheetNamee,bold)
		worksheet.write(0, col+4, "Fold of enrichment with "+SheetNamee,bold)
		for x in range(0,len(pvalue_shresholdlist)):
			worksheet.write(row,col+1,FinalOverlapGeneNumberList[x])
			worksheet.write(row,col+2,str(FinalOverlapGeneNameList[x]))
			pvalueofhypergeo=(stats.hypergeom.sf(FinalOverlapGeneNumberList[x]- 1,Population[Unit],len(ReferenceGeneNameNew),TotalGeneNumberList[x]))
			if pvalueofhypergeo<=0.05:
				color=red
			elif pvalueofhypergeo<=0.1:
				color=yellow
			else:
				color=black
			worksheet.write(row,col+3,pvalueofhypergeo,color)
			print (FinalOverlapGeneNumberList[x],Population[Unit],len(ReferenceGeneNameNew),TotalGeneNumberList[x])
			if (len(ReferenceGeneNameNew)==0) or (float(TotalGeneNumberList[x]))==0:
				worksheet.write(row,col+4,0)
			else:
				worksheet.write(row,col+4,(float(FinalOverlapGeneNumberList[x])/float(TotalGeneNumberList[x]))/(float(len(ReferenceGeneNameNew))/float(Population[Unit])))
			row=row+1


##############################################################################			
	row=1
	col=0
	for x in range(0,len(pvalue_shresholdlist)):
		worksheet.write(row,col,pvalue_shresholdlist[x])
		worksheet.write(row,col+2,TotalGeneNumberList[x])
		worksheet.write(row,col+1,Qvalue_shresholdlist[x])
		row=row+1
workbook.close()
print "ReferenceGeneNameNumberList=",ReferenceGeneNameNumberList
###############END#############
