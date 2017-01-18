#! /usr/bin/perl

use POSIX;
use warnings;
use strict;
my $infile = shift;

open INPUT, $infile or die "can't open file\n";
#read coordinates list file
while(<INPUT>){
	chomp;
	my @array=split(/\t/,$_);
	print substr($array[9],33,19)."\n";
}


