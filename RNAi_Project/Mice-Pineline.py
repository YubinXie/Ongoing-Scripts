import os
import subprocess

#os.chdir("/media/yubin/C2F69FFCF69FEF43/sRNAProject/SRNA_Yubin/")
ProjectDirectory = "/media/yubin/C2F69FFCF69FEF43/sRNAProject/"
FileDirectory="SRNA_Yubin/AllDrugResistance/Fasta"
os.chdir(ProjectDirectory)
os.chdir(FileDirectory)

Xmer = "19"
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

if GroupOption=="B":
	CaseName = "B-DrugResistance." 
	AllName = "BC-All."
	CaseFastaName = "B-group-rightsidesignificantreads-" #"B-group-rightsidesignificantreads-" #"AB-group-rightsidesignificantreads-"
	AllFastaName = "BC-" #BC- #All-
	CaseCountFileName="B-group-19mer-counts.txt"
	AllCountFileName="BC-group-19mer-counts.txt"
	CaseAllratio= "0.0177" #Group B

if GroupOption=="AB":
	CaseName = "AB-DrugResistance." 
	AllName = "All."
	CaseFastaName = "AB-group-rightsidesignificantreads-" #"B-group-rightsidesignificantreads-" #"AB-group-rightsidesignificantreads-"
	AllFastaName = "All-" #BC- #All-
	CaseCountFileName="AB-group-19mer-counts.txt"
	AllCountFileName="All-19mer-counts.txt"
	CaseAllratio="0.0181" #Group AB

#CaseFastaName="drugvcase-rightside-enriched"


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

def main():
	#GenerateFasta(Xmer)
	#Mapping()
	#Formating()
	#MultiHitting()
	ReadsWeightCounting()
	#AlignmentWeightCounting()
	#Counting()
	#Binomoral()
	CountWeightBinomoral()
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

def ReadsWeightCounting():
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

if __name__ == '__main__':
	main()