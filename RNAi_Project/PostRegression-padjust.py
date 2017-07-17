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

(opts, args) = optParser.parse_args()

OutputFile = opts.InputFile.replace(".txt","-PvalueAdjusted.txt")


def main():

	with open (opts.InputFile,"r") as openInputFile:
		PValueList=[]
		next(openInputFile)
		for line in openInputFile:
			ElementList=line.strip("\n").split("\t")
			PValue=ElementList[7]
			PValueList.append(PValue)

	P_adjustList = Rstats.p_adjust(FloatVector(PValueList), method = 'fdr')


	with open (opts.InputFile,"r") as openInputFile, open (OutputFile,"w+") as OpenOutputFile :
		NumberOrder=-2
		#print NumberOrder
		#OpenOutputAdjustedFile.writelines(("%s\tP Adjust(fdr)\n") % OpenOutputFile.readline().strip("\n"))
		for line in openInputFile:
			NumberOrder +=1
			#print NumberOrder
			Line=line.strip("\n")
			if NumberOrder==-1:
				OpenOutputFile.writelines(("%s\tP Adjust(fdr)\n")% Line)
				continue
			PAdjust=P_adjustList[NumberOrder]
			OpenOutputFile.writelines(("%s\t%s\n")% (Line, PAdjust))
				

	stop = timeit.default_timer()
	print stop - start, "seconds. Done"
	




if __name__ == "__main__":
   main()
