import os
import subprocess

#os.chdir("/media/yubin/C2F69FFCF69FEF43/sRNAProject/SRNA_Yubin/")
ProjectDirectory = "/media/yubin/C2F69FFCF69FEF43/sRNAProject/"
FileDirectory="SRNA_Yubin/Drugv/Experiment/"
os.chdir(ProjectDirectory)
os.chdir(FileDirectory)
#XmerList = ["18"]
XmerList = ["15","16","17","18","19"]
ReadsList= ["100"]#["100","200","300","400","500","700","800","900","1000"]
Mismatch = "3"
CaseName = "Drugv."
#CaseName = "Top.Drugv."
AllCaseName= "AllDrugv."
AllName = "All."


CaseFastaName="../X-merData/drugvcase-rightside-enriched"
#CaseFastaName="../X-merData/Top-enriched-rightside"
AllFastaName = "../X-merData/all-"
AllCaseFastaName="../X-merData/drugvcase-wholereads"
CaseCountFileName="../X-merData/drugvcase-counts-counts.txt"
AllCountFileName="../X-merData/all-unique-counts.txt"
WeightType="-ReadODWeighted.txt" #-region.txt
	
CaseAllratio="0.0696" #DrugV
SamFileName = ""
#SamFileName="-weight"
MultiHit = "2"
#MultiHit=""
#if MultiHit != "":
#	SamFileName="-LimitMultiHit-" + MultiHit


def main():
	Initialization="F"
	if Initialization=="T":
		print "Generating X-mer..."
		print "Generating X-mer for All DrugV reads"
		GenerateXmer(AllCaseFastaName,Xmer)
		print "Generating X-mer for enriched DrugV reads"
		GenerateXmer(CaseFastaName,Xmer)
		print "Generating X-mer for enriched DrugV reads"
		GenerateXmer(AllFastaName,Xmer)

		print "Mapping to transcriptome..."
		print "Mapping enriched DrugV to transcriptome..."
		Mapping(CaseOutputFolder,CaseFastaName,Mismatch,Xmer)
		print "Formating enriched DrugV reads..."
		Formating(CaseOutputFolder,CaseFastaName)
		print "Mapping All DrugV to transcriptome..."
		Mapping(AllCaseOutputFolder,AllCaseFastaName,Mismatch,Xmer)
		print "Formating All DrugV reads..."
		Formating(AllCaseOutputFolder,AllCaseOutputName)
		print "Mapping All reads to transcriptome..."
		Mapping(AllOutputFolder,AllFastaName,Mismatch,Xmer) 
		print "Formating All reads..."
		Formating(AllOutputFolder,AllOutputFolder)


	UniqueAlignmentCounting="F"
	if UniqueAlignmentCounting=="T":

	#GenerateFasta(ReadsFile)
	#GenerateFasta(Xmer)
	#GenerateXmer(ReadFasta,Xmer)
	#Mapping(TopReadOutputFolder,ReadFasta,Mismatch,Xmer)
	#Formating(TopReadOutputFolder,TopReadOutputName)
	#Counting(TopReadOutputFolder,TopReadOutputName)
	#Annotation(TopReadOutputFolder,TopReadOutputName,"")
	#Regression(AllCaseOutputFolder,AllCaseOutputName)
	#Regression_Bi(AllCaseOutputFolder,AllCaseOutputName)  #
	#Padjust_Regression(AllCaseOutputFolder,AllCaseOutputName,"-Bi")
	#Annotation(AllCaseOutputFolder,AllCaseOutputName,"-ReadODRegression-Regression-Bi-PvalueAdjusted.txt")
	#ReadsODRegressionCounting(AllCaseOutputFolder,AllCaseOutputName)

	#MultiCounting(CaseOutputFolder,CaseOutputName)
	#MultiCounting(AllOutputFolder,AllOutputName)
	Binomoral(AllOutputFolder,AllOutputName,CaseOutputFolder,CaseOutputName,CaseAllratio,"Multicount")

	AllCase="F"
	if AllCase=="T": 
		GenerateXmer(AllCaseFastaName,Xmer)
		Mapping(AllCaseOutputFolder,AllCaseFastaName)
		Formating(AllCaseOutputFolder,AllCaseOutputName)
		Counting(AllCaseOutputFolder,AllCaseOutputName)

	#Mapping(CaseOutputFolder,CaseFastaName)
	#Mapping(AllOutputFolder,AllFastaName)
	#Formating(AllCaseOutputFolder,AllCaseOutputName)
	#ReadsODWeightCounting()
	#ReadsODWeightCounting(ReadsODWeightFileName,AllCaseFastaName,AllCaseOutputFolder,AllCaseOutputName)
	#MultiHitting()
	#WeightCounting()
	#ReadsWeightCounting()
	#Counting()
	ReginCount ="F"
	if ReginCount == "T":
		RegionCounting(CaseOutputFolder,CaseOutputName)
		RegionNumberCount(CaseOutputFolder,CaseOutputName)
		Annotation(CaseOutputFolder,CaseOutputName,"-region-count.txt")
		RegionNumberDivideLength(CaseOutputFolder,CaseOutputName)

		RegionCounting(AllOutputFolder,AllOutputName)
		RegionNumberCount(AllOutputFolder,AllOutputName)
		Annotation(AllOutputFolder,AllOutputName,"-region-count.txt")
		RegionNumberDivideLength(AllOutputFolder,AllOutputName)
	#Binomoral()
	#CountWeightBinomoral()
	#Annotation()
	#Annotation(AllCaseOutputFolder,AllCaseOutputName,WeightType)
	#Annotation(CaseOutputFolder,CaseOutputName,"-region-count.txt")


def GenerateFasta(ReadsFile):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Convert-to-Fasta.py " + ReadsFile
	running(commend)


def GenerateXmer(Fastafile,X):
	print "Generating ",X,"-mer file"
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py " + Fastafile + "19mer.fa " + X
		
	running(commend)

def Mapping(OutputFolder,FastaName,Mismatch,Xmer):
	print "Mapping ",FastaName,Xmer, "-mer to transcriptome with ",Mismatch, " mismatch"
	commend = "tophat2 -N " + Mismatch + " --read-edit-dist " + Mismatch + " --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + OutputFolder + " " + ProjectDirectory + "genome/GRCh38.genome " + FastaName+str(Xmer) + "mer.fa"
	running(commend)

def Formating(OutputFolder,OutputName):
	
	commend = "samtools sort -o " + OutputFolder + "accepted_hits.sort.bam " + OutputFolder + "accepted_hits.bam"
	running(commend)
	commend = "samtools sort -o " + OutputFolder + OutputName + ".sam " + OutputFolder + "accepted_hits.sort.bam"
	running(commend)


def WeightCounting():
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weight.py -s no -i gene_id -q -a 0 " + CaseOutputFolder + CaseOutputName +".sam " + "../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "  + CaseOutputFolder + CaseOutputName +"-weight.txt"
	running(commend)
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weight.py -s no -i gene_id -q -a 0 " + AllOutputFolder + AllOutputName +".sam " + "../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "  + AllOutputFolder + AllOutputName +"-weight.txt"
	running(commend)

def ReadsWeightCounting():
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyreadscount.py -s no -i gene_id -q -a 0 -w "+ CaseCountFileName + " -d "+CaseFastaName + "19mer.fa " + CaseOutputFolder + CaseOutputName +".sam "  + ProjectDirectory + "referenceGenome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "  + CaseOutputFolder + CaseOutputName +"-ReadsWeighted.txt"
	running(commend)
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyreadscount.py -s no -i gene_id -q -a 0 -w "+ AllCountFileName + " -d "+AllFastaName + "19mer.fa " + AllOutputFolder + AllOutputName +".sam " + ProjectDirectory + "referenceGenome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "  + AllOutputFolder + AllOutputName +"-ReadsWeighted.txt"
	running(commend)	

def ReadsODWeightCounting(ReadsODWeightFileName,CaseFastaName,CaseOutputFolder,CaseOutputName):
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyreadOD.py -s no -i gene_id -q -a 0 -w "+ ReadsODWeightFileName + " -d "+CaseFastaName + "19mer.fa " + CaseOutputFolder + CaseOutputName +".sam "  + ProjectDirectory + "referenceGenome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "  + CaseOutputFolder + CaseOutputName +"-ReadODWeighted.txt"
	running(commend)

def ExtractMappedSequence(OutputFolder,OutputName):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Extract-Mapped-Seq.py -i "+ OutputFolder + OutputName + ".sam -r ../X-merData/drugvcase-wholereads19mer.fa -w ../X-merData/drugvcase-wholereads.txt"
	running(commend)

def ReadsODRegressionCounting(OutputFolder,OutputName):
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-OD-Regression.py -s no -i gene_id -q -a 0 -d "+OutputFolder + OutputName + "-MappedSequence.txt " + OutputFolder + OutputName +".sam "  + ProjectDirectory + "referenceGenome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "  + OutputFolder + OutputName +"-ReadODRegression.txt"
	running(commend)

def Regression(OutputFolder,OutputName):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Regression.py -i "+ OutputFolder + OutputName + "-ReadODRegression.txt -r "+ OutputFolder + OutputName + "-MappedSequence.txt"
	running(commend)

def Regression_Bi(OutputFolder,OutputName):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Regression-Bi.py -i "+ OutputFolder + OutputName + "-ReadODRegression.txt -r "+ OutputFolder + OutputName + "-MappedSequence.txt"
	running(commend)

def Padjust_Regression(OutputFolder,OutputName,Method):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/PostRegression-padjust.py -i "+ OutputFolder + OutputName + "-ReadODRegression-Regression" +Method+".txt"
	running(commend)

def Counting(OutputFolder,OutputName):
	
	commend = "htseq-count -s no -i gene_id -q " + OutputFolder + OutputName + ".sam " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > " + OutputFolder + OutputName + ".txt"
	running(commend)

def MultiCounting(OutputFolder,OutputName):
	
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-multicount.py -s no -i gene_id -q " + OutputFolder + OutputName + ".sam " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > " + OutputFolder + OutputName + "Multicount.txt"
	running(commend)

def RegionCounting(OutputFolder,OutputName):
	
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-region.py -s no -i gene_id -q " + OutputFolder + OutputName + ".sam " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > " + OutputFolder + OutputName + "-region.txt"
	running(commend)

def MultiHitting():
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/SelectMultiHit.py " + CaseOutputFolder + CaseOutputName + ".sam " + MultiHit
	running(commend)
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/SelectMultiHit.py " + AllOutputFolder + AllOutputName + ".sam " + MultiHit
	running(commend)

def Binomoral(AllOutputFolder,AllOutputName,CaseOutputFolder,CaseOutputName,CaseAllratio,Modification):
	
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + Modification+".txt " + CaseOutputFolder + CaseOutputName + Modification+ ".txt " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf " + CaseAllratio
	running(commend)

def CountWeightBinomoral():
	
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + "-ReadsWeighted.txt " + CaseOutputFolder + CaseOutputName + "-ReadsWeighted.txt " + ProjectDirectory + "referenceGenome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf " + CaseAllratio
	running(commend)

def RegionNumberCount(OutputFolder,OutputName):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Merge_Region.py -i " + OutputFolder + OutputName + "-region.txt"
	running(commend)

def RegionNumberDivideLength(OutputFolder,OutputName):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Divide-Length.py -i " + OutputFolder + OutputName + "-region-count_annotated.txt"
	running(commend)

def Annotation(OutputFolder,OutputName,WeightType):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Annotate_GeneID.py -i " + OutputFolder + OutputName + WeightType+" -r /media/yubin/C2F69FFCF69FEF43/sRNAProject/genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf"
	running(commend)

def running(commend):
	print commend
	process = subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.stdout.readlines()




for Xmer in XmerList:
	for Reads in ReadsList:
		ReadsFile="../X-merData/Top" + Reads + "-enriched-rightside19mer.txt"
		ReadFasta="../X-merData/Top" + Reads + "-enriched-rightside"
		TopReadOutputFolder="Top" + Reads + "."+Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
		TopReadOutputName="Top" + Reads +"."+ Xmer + "mer." + Mismatch + "mis.genome.new.trans" + SamFileName
		AllCaseOutputFolder = AllCaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
		ReadsODWeightFileName = "../X-merData/drugvcase-wholereads.txt"
		CaseOutputFolder = CaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
		AllOutputFolder = AllName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"

		CaseOutputName = CaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans" + SamFileName
		AllOutputName = AllName + Xmer + "mer." + Mismatch + "mis.genome.new.trans"+ SamFileName
		AllCaseOutputName = AllCaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans" + SamFileName
		if __name__ == '__main__':
			main()