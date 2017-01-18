from vcf_parser import VCFParser
my_parser = VCFParser(infile='../Files/example.vcf', split_variants=True,check_info=True)
for line in my_parser.metadata.print_header():
    print(line)
for variant in my_parser:
	#print variant
    print('\t'.join([[variant[head] for head in my_parser.header]]))