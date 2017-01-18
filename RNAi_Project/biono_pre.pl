#!/usr/bin/perl -w
use strict;

my $control = $ARGV[0];
my $infile = $ARGV[1];
my $outfile1=$ARGV[2];
my $ratio= $ARGV[3];
if (!defined $infile && !defined $control && !defined $ratio) {
    die "Usage: $0 control infile output ratio\n";
}
open (IN, "$infile") or die "Cannot open $infile\n";
open (OUT1, ">$outfile1") or die "Cannot write $outfile1\n";
open (CONTROL, "$control") or die "Cannot open $control\n";

###########################################################
my @lin=();
my $genename_c = "";
my %genenumber_c =();
while (<CONTROL>) {
        chomp () ;
        @lin = split /\t/, $_;
        $genename_c=$lin[0];
        $genenumber_c{$genename_c}= $lin[2];          
}

###########################################################

my @lin2 =();

while( <IN>){ 
chomp();    
@lin2 = split /\t/, $_;
   if (exists $genenumber_c{$lin2[0]}){
    print OUT1 "$lin2[0]\t$lin2[1]\t$lin2[2]\t$genenumber_c{$lin2[0]}\t$ratio\n";
     }
else {print "$genenumber_c{$lin2[0]} does not exist \n "; }
}
    
close IN;
close OUT1;
close CONTROL;
