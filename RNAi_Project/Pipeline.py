

python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py drugvcase-rightside-enriched19mer.fa 16

python ~/Dropbox/Linux/scripts/RNAi_Project/Generate-Xmer.py all-19mer.fa 16

tophat2 -N 3 --read-edit-dist 3 --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index ../genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o Drugv.16mer.3mis.genome.new.trans.out ../genome/GRCh38.genome drugvcase-rightside-enriched16mer.fa

tophat2 -N 3 --read-edit-dist 3 --num-thread 8 --max-multihits 10000 --report-secondary-alignments --GTF ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf --transcriptome-index ../genome/gencode.v24.chr_patch_hapl_scaff.annotation --transcriptome-max-hits 10000 --transcriptome-only -o All.16mer.3mis.genome.new.trans.out ../genome/GRCh38.genome all-16mer.fa 

cd Drugv.16mer.3mis.genome.new.trans.out/

samtools sort -o accepted_hits.sort.bam accepted_hits.bam

samtools view -o drugv.16mer.3mis.genome.new.trans.sam accepted_hits.sort.bam

cd ../All.16mer.3mis.genome.new.trans.out

samtools sort -o accepted_hits.sort.bam accepted_hits.bam

samtools view -o xxxx.sam accepted_hits.sort.bam

htseq-count -s no -i gene_id Drugv.16mer.3mis.genome.new.trans.out/drugv.16mer.3mis.genome.new.trans.sam ../genome/gencode.v24.chr_patch_hapl_scaff.annotation.gtf > Drugv.16mer.3mis.genome.new.trans.out/drugv.16mer.3mis.genome.new.trans.txt 


