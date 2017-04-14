import os
import subprocess

#os.chdir("/media/yubin/C2F69FFCF69FEF43/sRNAProject/SRNA_Yubin/")
ProjectDirectory = "/media/yubin/C2F69FFCF69FEF43/sRNAProject/"
FileDirectory="SRNA_Yubin/Drugv/Experiment/"
os.chdir(ProjectDirectory)
os.chdir(FileDirectory)
Xmer = "19"
Mismatch = "3"
CaseName = "Drugv."
AllName = "All."

CaseFastaName="../X-merData/drugvcase-rightside-enriched"
AllFastaName = "../X-merData/all-"
CaseCountFileName="../X-merData/drugvcase-counts-counts.txt"
AllCountFileName="../X-merData/all-unique-counts.txt"

CaseOutputFolder = CaseName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
AllOutputFolder = AllName + Xmer + "mer." + Mismatch + "mis.genome.new.trans.out/"
CaseAllratio="0.0696" #DrugV
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
	#WeightCounting()
	ReadsWeightCounting()
	#Counting()
	#Binomoral()
	CountWeightBinomoral()

def GenerateFasta(X):
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py X-merData/drugvcase-rightside-enriched19mer.fa " + X
	running(commend)
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py X-merData/All-19mer.fa " + X
	running(commend)

def Mapping():
	commend = "tophat2 -N " + Mismatch + " --read-edit-dist " + Mismatch + " --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + CaseOutputFolder + " " + ProjectDirectory + "genome/GRCh38.genome " + CaseFastaName+str(Xmer) + "mer.fa"
	running(commend)
	commend = "tophat2 -N " + Mismatch + " --read-edit-dist " + Mismatch + " --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + AllOutputFolder + " " + ProjectDirectory + "genome/GRCh38.genome " + AllFastaName + str(Xmer) + "mer.fa"
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

def Counting():
	
	commend = "htseq-count -s no -i gene_id -q " + CaseOutputFolder + CaseOutputName + ".sam " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > " + CaseOutputFolder + CaseOutputName + ".txt"
	running(commend)
	commend = "htseq-count -s no -i gene_id -q " + AllOutputFolder + AllOutputName + ".sam " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > " + AllOutputFolder + AllOutputName + ".txt"
	running(commend)

def MultiHitting():
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/SelectMultiHit.py " + CaseOutputFolder + CaseOutputName + ".sam " + MultiHit
	running(commend)
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/SelectMultiHit.py " + AllOutputFolder + AllOutputName + ".sam " + MultiHit
	running(commend)

def Binomoral():
	
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + ".txt " + CaseOutputFolder + CaseOutputName + ".txt " + ProjectDirectory + "genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf " + CaseAllratio
	running(commend)

def CountWeightBinomoral():
	
	commend = "python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + "-ReadsWeighted.txt " + CaseOutputFolder + CaseOutputName + "-ReadsWeighted.txt " + ProjectDirectory + "referenceGenome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf " + CaseAllratio
	running(commend)

def running(commend):
	print commend
	process = subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.stdout.readlines()

if __name__ == '__main__':
	main()