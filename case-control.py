import vcf
import subprocess


vcf_reader = vcf.Reader(open('../Files/example.vcf', 'r'))
#record = next(vcf_reader)
SampleNameList=vcf_reader.samples
Commend=""
NumberPlus=0
NumberMinus=0
NumberZero=0
Case=[]
CaseString=""
Control=[]
ControlString=""
for sample in SampleNameList:
	if "A" in sample:
		Commend=Commend+"+"
		Case.append(sample)
		NumberPlus=NumberPlus+1
		CaseString=CaseString+sample+","
	elif "B" in sample:
		Commend=Commend+"-"
		Control.append(sample)
		NumberMinus=NumberMinus+1
		ControlString=ControlString+sample+","
	else:
		Commend=Commend+"0"
		NumberZero=NumberZero+1
print Commend
print NumberPlus, NumberMinus, NumberZero,Case,Control
print CaseString
print ControlString

CaseCommendLine="bcftools view -s " + CaseString+ " MIGen_ExS_28K.v6.ATVB_NoDup.vcf.gz | bgzip -c > MIGen_ExS_28K.v6.ATVB_NoDup_Case.vcf.gz"
ControlCommendLine="bcftools view -s " + ControlString+ " MIGen_ExS_28K.v6.ATVB_NoDup.vcf.gz | bgzip -c > MIGen_ExS_28K.v6.ATVB_NoDup_Control.vcf.gz"
CommendLine= CaseCommendLine + " && " + ControlCommendLine

#subprocess.Popen(CommendLine,shell=True)