#!/usr/bin/bash

module load samtools/1.2
module load HTSeq/0.5.4p5

for i in *out;
do 
echo working $i
cd $i
samtools sort accepted_hits.bam accepted_hits.sort
samtools view accepted_hits.sort.bam >accepted_hits.sort.sam
htseq-count -s no -i gene_id -m intersection-nonempty -q accepted_hits.sort.sam /group/xhe-lab/zifeng/data/age/genomemap/gencode.vM9.chr_patch_hapl_scaff.annotation.gtf >$i.accepted_hits_counts_by_gene.txt
cd /group/xhe-lab/zifeng/data/age/for_zifeng_temp
/group/xhe-lab/zifeng/cancer/mouse.genome
