import timeit;
start = timeit.default_timer()
import sys, optparse
import re
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show , legend
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
Rstats = importr('stats')
usage="python xx.py -i inputfile"
optParser = optparse.OptionParser(usage=usage)

optParser.add_option( "-i", "--input", type="string", dest="InputFile",
      default = "", help = "" )

optParser.add_option( "-r", "--reference", type="string", dest="ReferenceFile",
      default = "", help = "" )


(opts, args) = optParser.parse_args()

OutputFile = opts.InputFile.replace(".txt","-Regression-OD.txt")
OutputFile_Padjust=OutputFile.replace(".txt","-PvalueAdjusted.txt")

ReadDic={}

def main():
	with open (opts.ReferenceFile) as OpenReferenceFile:
		for line in OpenReferenceFile:
			ElementList=line.strip("\n").split("\t")
			ReadID=ElementList[0]
			Weight=ElementList[3]
			ReadDic[ReadID]=float(Weight)
	#CopyReadDic=ReadDic

	with open (opts.InputFile,"r") as openInputFile, open (OutputFile,"w+") as openOutputFile:
		PValueList=[]
		openOutputFile.write("GeneID\t# UnMapped\t # Mapped\t# SignificantMapped\tslope\tintercept\tr_value\tp_value\tstd_err\n")
		for line in openInputFile:
			NumberofNon0=0
			NotMappedList=[]
			ElementList = line.strip("\n").split("\t")
			NotMappedOutputList=[] 
			if len(ElementList)<=2 or ElementList[1] =="0":
				continue
			else:
				MappedList=ElementList[2].replace("[","").replace("]","").split(";")
				MappedReadList=[]
				UnMappedReadDic=dict(ReadDic)
		
				for element in MappedList:
					elementList=element.replace("'","").split(",")
					MappedReadList.append(float(elementList[1]))
					#print elementList[1]
					#print elementList[1]==" 0"
					if elementList[1] != " 0":
						NumberofNon0+=1
					del UnMappedReadDic[elementList[0]]
				UnMappedList=UnMappedReadDic.values()
				NumberofUnmapped=len(UnMappedReadDic)
				NUmberofMapped=len(MappedReadList)
				#print NumberofUnmapped,NUmberofMapped,NumberofUnmapped+NUmberofMapped
				Xi=[0]*NumberofUnmapped + [1]*NUmberofMapped
				Yi=UnMappedList + MappedReadList

				(a_s,b_s,r,pvalue,stderr)=stats.linregress(Xi,Yi)
				PValueList.append(pvalue)

				#print a_s,b_s,r,tt,stderr
				#print MappedReadList
				#for read, weight in ReadDic.items():
					#print read, weight
					#if read not in MappedReadList:
						
						#NotMappedOutputList.append(weight)
						#print NotMappedOutputList
				#print ElementList[2],";".join(str(x) for x in NotMappedOutputList)
				openOutputFile.writelines("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (ElementList[0],NumberofUnmapped,NUmberofMapped,NumberofNon0,a_s,b_s,r,pvalue,stderr))	

	stop = timeit.default_timer()
	print stop - start, "seconds. Done"
	




if __name__ == "__main__":
   main()
