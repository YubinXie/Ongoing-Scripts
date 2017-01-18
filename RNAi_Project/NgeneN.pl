#!/usr/bin/perl -w
use strict;

my $infile = $ARGV[0];
#my $contig= "/group/xhe-lab/zifeng/cancer/gencode.v24.transcripts.fa";
my $contig= "/group/xhe-lab/zifeng/cancer/gencode.vM9.transcripts.fa";
#$mapfile = $ARGV[1];
my $outfile1 = "probelist";
my $outfile2 = "genelist";
if (!defined $infile) {
    die "Usage: $0 infile\n";
}
open (IN, "$infile") or die "Cannot open $infile\n";
open (OUT1, ">$outfile1") or die "Cannot write $outfile1\n";
open (OUT2, ">$outfile2") or die "Cannot write $outfile2\n";

open (CONTIG, "$contig") or die "Cannot open $contig\n";

###########################################################

my $seq_name = $1 ;
my $seq = '' ;
#my %contig_seq = () ;
my %contig_seqlength = () ;

while (<CONTIG>) {
    
    if (/^>(\S+)/) {
        $seq_name = $1 ;
        $seq_name =~ tr /\|/_/;
        while (<CONTIG>) {
            chomp ;
            
            if (/^>(\S+)/) {
                $seq_name =~ tr /\|/_/;
		#print "$seq_name\n" ;
                
                #$contig_seq{$seq_name} = $seq ;
                $contig_seqlength{$seq_name} = length($seq) ;
                $seq_name = $1 ;
                $seq = '' ;
            }
            else {
                $seq .= $_ ;
            }
            
        }
        
    }
}

#$contig_seq{$seq_name} = $seq ;
$contig_seqlength{$seq_name} = length($seq) ;

###########################################################

my @lin =();
my $probe ="";
my $gene = "";
my %probefreq =();
my %genefreq =();
my @genes =();
my @probes =();

while( <IN>){ 
    @lin = split /\s+/, $_;
    $probe = $lin[0];
    $gene= $lin[2];
    $gene =~ tr/\|/_/;
 #   print "$gene\n";
    if (! grep /^$probe$/, @probes) {
        push @probes, $probe;
	$probefreq{$probe}=1;
    }
    else {
	$probefreq{$probe}++;
    }
    if (!grep /^$gene$/, @genes) {
	push @genes,$gene;
        $genefreq{$gene}=1;
    }
    else {
	$genefreq{$gene}++;
    }
}

foreach $probe (@probes) {
    print OUT1 "$probe\t$probefreq{$probe}\n";
}
my $ratio = "";
#print "********\n ";
#print "the following @genes \n";

foreach $gene (@genes) {
   if(exists $genefreq{$gene} && exists $contig_seqlength{$gene}){  
    $ratio=$genefreq{$gene}/$contig_seqlength{$gene};
   }
   else {print "$genefreq{$gene} does not exists\n";}
    $ratio= sprintf "%.5f", $ratio;
    print OUT2 "$gene\t$contig_seqlength{$gene}\t$genefreq{$gene}\t$ratio\n";
} 
    
close IN;
close OUT1;
close OUT2;
close CONTIG;
