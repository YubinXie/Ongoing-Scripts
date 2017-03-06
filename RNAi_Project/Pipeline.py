import os
import subprocess

os.chdir("/media/yubin/C2F69FFCF69FEF43/sRNAProject/SRNA_Yubin/")
Xmer="15"
Mismatch="3"
CaseName="Drugv."
AllName="All."

CaseFastaName="drugvcase-rightside-enriched"
AllFastaName="all-"

CaseOutputFolder="Drugv."+ Xmer +"mer."+Mismatch+ "mis.genome.new.trans.out/"
AllOutputFolder="All."+ Xmer +"mer."+Mismatch+"mis.genome.new.trans.out/"

MultiHit="-LimitMultiHit-5"

CaseOutputName=CaseName+ Xmer +"mer."+Mismatch+ "mis.genome.new.trans" + MultiHit
AllOutputName=AllName+ Xmer +"mer."+Mismatch+ "mis.genome.new.trans"+ MultiHit

def main():
	#GenerateFasta(Xmer)
	#Mapping()
	#Formating()
	#Counting()
	Binomoral()

def GenerateFasta(X):
	commend="python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py drugvcase-rightside-enriched19mer.fa " + X
	running(commend)
	commend="python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py all-19mer.fa " + X
	running(commend)

def Mapping():
	commend="tophat2 -N " +Mismatch+" --read-edit-dist " +Mismatch+" --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index ../genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + CaseOutputFolder + " ../genome/GRCh38.genome " + CaseFastaName+str(Xmer)+"mer.fa"
	running(commend)
	commend="tophat2 -N " +Mismatch+" --read-edit-dist " +Mismatch+" --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index ../genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o " + AllOutputFolder + " ../genome/GRCh38.genome "+ AllFastaName+str(Xmer)+"mer.fa"
	running(commend)

def Formating():
	commend="samtools sort -o " + CaseOutputFolder + "accepted_hits.sort.bam " + CaseOutputFolder+ "accepted_hits.bam"
	running(commend)
	commend="samtools sort -o " + CaseOutputFolder + CaseOutputName +".sam "+ CaseOutputFolder+ "accepted_hits.sort.bam"
	running(commend)
	commend="samtools sort -o " + AllOutputFolder + "accepted_hits.sort.bam " + AllOutputFolder+ "accepted_hits.bam"
	running(commend)
	commend="samtools sort -o " + AllOutputFolder + AllOutputName +".sam "+ AllOutputFolder+ "accepted_hits.sort.bam"
	running(commend)

def Counting():
	commend="htseq-count -s no -i gene_id -q " + CaseOutputFolder + CaseOutputName +".sam ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "+ CaseOutputFolder + CaseOutputName + ".txt"
	running(commend)
	commend="htseq-count -s no -i gene_id -q " + AllOutputFolder + AllOutputName +".sam ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > "+ AllOutputFolder + AllOutputName + ".txt"
	running(commend)

def Binomoral():
	commend="python ~/Dropbox/Linux/scripts/RNAi_Project/Genome_HTSeq/Binormal_HTseq.py " + AllOutputFolder + AllOutputName + ".txt " + CaseOutputFolder + CaseOutputName + ".txt ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf 0.0696"
	running(commend)

def running(commend):
	print commend
	process=subprocess.Popen(commend,shell=True,stdout=subprocess.PIPE)
	process.wait()
	print process.stdout.readlines()

if __name__ == '__main__':
	main()