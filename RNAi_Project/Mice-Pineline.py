import os
import subprocess

#os.chdir("/media/yubin/C2F69FFCF69FEF43/sRNAProject/SRNA_Yubin/")
ProjectDirectory = "/media/yubin/C2F69FFCF69FEF43/sRNAProject/"
FileDirectory="SRNA_Yubin/AllDrugResistance/Fasta"
os.chdir(ProjectDirectory)
os.chdir(FileDirectory)

XmerList = ["15","16","17","18","19"]
Mismatch = "3"




GroupOption="B"

if GroupOption=="A":
	CaseName = "A-DrugResistance." 
	AllName = "AC-All."
	CaseFastaName = "A-group-rightsidesignificantreads-" #"B-group-rightsidesignificantreads-" #"AB-group-rightsidesignificantreads-"
	AllFastaName = "AC-" #BC- #All-
	CaseAllratio="0.0184"
	CaseCountFileName="A-group-19mer-counts.txt"
	AllCountFileName="AC-group-19mer-counts.txt"
	ReadsORWeightFileName = "X-merData/A-group-19mer-wholereads.txt"

if GroupOption=="B":
	CaseName = "B-DrugResistance." 
	AllName = "BC-All."
	CaseFastaName = "B-group-rightsidesignificantreads-" #"B-group-rightsidesignificantreads-" #"AB-group-rightsidesignificantreads-"
	AllFastaName = "BC-" #BC- #All-
	CaseCountFileName="B-group-19mer-counts.txt"
	AllCountFileName="BC-group-19mer-counts.txt"
	CaseAllratio= "0.0177" #Group B
	ReadsORWeightFileName = "X-merData/B-group-19mer-wholereads.txt"

if GroupOption=="AB":
	CaseName = "AB-DrugResistance." 
	AllName = "All."
	CaseFastaName = "AB-group-rightsidesignificantreads-" #"B-group-rightsidesignificantreads-" #"AB-group-rightsidesignificantreads-"
	AllFastaName = "All-" #BC- #All-
	CaseCountFileName="AB-group-19mer-counts.txt"
	AllCountFileName="All-19mer-counts.txt"
	CaseAllratio="0.0181" #Group AB
	ReadsORWeightFileName = "X-merData/AB-group-19mer-wholereads.txt"

#CaseFastaName="drugvcase-rightside-enriched"




def main():
	#GenerateFasta(Xmer)
	#Mapping()
	#Formating()
	#MultiHitting()
	#RegionCounting(CaseOutputFolder,CaseOutputName)
	#ReadsORWeightCounting(ReadsORWeightFileName,CaseFastaName,CaseOutputFolder,CaseOutputName)
	Annotation(CaseOutputFolder,CaseOutputName,"-ReadORWeighted.txt")
	#ReadsWeightCounting()
	#AlignmentWeightCounting()
	#Counting()
	#Binomoral()
	#CountWeightBinomoral()

def GenerateFasta(X):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py X-merData/drugvcase-rightside-enriched19mer.fa " + X
	running(commend)
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py X-merData/All-19mer.fa " + X
	running(commend)

def Mapping():
	commend = "tophat2 -N " + Mismatch + " --read-edit-dist " + Mismatch + " --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + CaseOutputFolder + " " + ProjectDirectory + "referenceGenome/GRCm38.p5.genome " + CaseFastaName+str(Xmer) + "mer.fa"
	running(commend)
	commend = "tophat2 -N " + Mismatch + " --read-edit-dist " + Mismatch + " --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + AllOutputFolder + " " + ProjectDirectory + "referenceGenome/GRCm38.p5.genome " + AllFastaName + str(Xmer) + "mer.fa"
	running(commend)

def Formating():
	
	commend = "samtools sort -o " + CaseOutputFolder + "accepted_hits.sort.bam " + CaseOutputFolder + "accepted_hits.bam"
	running(commend)
	commend = "samtools sort -o " + CaseOutputFolder + CaseOutputName + ".sam " + CaseOutputFolder + "accepted_hits.sort.bam"
	running(commend)
	commend = "samtools sort -o " + AllOutputFolder + "accepted_hits.sort.bam " + AllOutputFolder + "accepted_hits.bam"
	running(commend)
	commend = "samtools sort -o " + AllOutputFolder + AllOutputName + ".sam " + AllOutputFolder + "accepted_hits.sort.bam"
	running(commend)

def ReadsWeightCounting(CaseCountFileName,CaseFastaName,CaseOutputFolder):
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyreadscount.py -s no -i gene_id -q -a 0 -w "+ CaseCountFileName + " -d "+CaseFastaName + "19mer.fa " + CaseOutputFolder + CaseOutputName +".sam "  + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > "  + CaseOutputFolder + CaseOutputName +"-ReadsWeighted.txt"
	running(commend)
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyreadscount.py -s no -i gene_id -q -a 0 -w "+ AllCountFileName + " -d "+AllFastaName + "19mer.fa " + AllOutputFolder + AllOutputName +".sam " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > "  + AllOutputFolder + AllOutputName +"-ReadsWeighted.txt"
	running(commend)

def AlignmentWeightCounting():
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyalignment.py -s no -i gene_id -q -a 0 " + CaseOutputFolder + CaseOutputName +".sam "  + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > "  + CaseOutputFolder + CaseOutputName +"-weight.txt"
	running(commend)
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyalignment.py -s no -i gene_id -q -a 0 " + AllOutputFolder + AllOutputName +".sam " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > "  + AllOutputFolder + AllOutputName +"-weight.txt"
	running(commend)

def Counting():
	
	commend = "htseq-count -s no -i gene_id -q " + CaseOutputFolder + CaseOutputName + ".sam " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > " + CaseOutputFolder + CaseOutputName + ".txt"
	running(commend)
	commend = "htseq-count -s no -i gene_id -q " + AllOutputFolder + AllOutputName + ".sam " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > " + AllOutputFolder + AllOutputName + ".txt"
	running(commend)

def MultiHitting():
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/SelectMultiHit.py " + CaseOutputFolder + CaseOutputName + ".sam " + MultiHit
	running(commend)
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/SelectMultiHit.py " + AllOutputFolder + AllOutputName + ".sam " + MultiHit
	running(commend)

def RegionCounting(OutputFolder,OutputName):
	
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-region.py -s no -i gene_id -q " + OutputFolder + OutputName + ".sam " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > " + OutputFolder + OutputName + "-region.txt"
	running(commend)

def ReadsORWeightCounting(ReadsORWeightFileName,CaseFastaName,CaseOutputFolder,CaseOutputName):
	commend = "python ~/tools/HTSeq-0.6.1/HTSeq/scripts/count-weightbyreadOR.py -s no -i gene_id -q -a 0 -w "+ ReadsORWeightFileName + " -d "+CaseFastaName + "19mer.fa " + CaseOutputFolder + CaseOutputName +".sam "  + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf > "  + CaseOutputFolder + CaseOutputName +"-ReadORWeighted.txt"
	running(commend)


def CountWeightBinomoral():
	
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + "-ReadsWeighted.txt " + CaseOutputFolder + CaseOutputName + "-ReadsWeighted.txt " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf " + CaseAllratio
	running(commend)

def Binomoral():
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + ".txt " + CaseOutputFolder + CaseOutputName + ".txt " + ProjectDirectory + "referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf " + CaseAllratio
	running(commend)

def running(commend):
	print commend
	process = subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.stdout.readlines()

def Annotation(OutputFolder,OutputName,WeightType):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Annotate_GeneID.py -i " + OutputFolder + OutputName + WeightType+" -r /media/yubin/C2F69FFCF69FEF43/sRNAProject/referenceGenome/gencode.vM13.chr_patch_hapl_scaff.annotation.gtf"
	running(commend)


for Xmer in XmerList:

	CaseOutputFolder = CaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
	AllOutputFolder = AllName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
	
	#CaseAllratio="0.0696" #DrugV
	SamFileName = ""
	#SamFileName="-weight"
	MultiHit = "2"
	#MultiHit=""
	#if MultiHit != "":
	#	SamFileName="-LimitMultiHit-" + MultiHit
	CaseOutputName = CaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans" + SamFileName
	AllOutputName = AllName + Xmer + "mer." + Mismatch + "mis.genome.new.trans"+ SamFileName
	
	if __name__ == '__main__':
		main()