import timeit;
start = timeit.default_timer()
import sys, optparse
import re
usage="python xx.py -i inputfile"
optParser = optparse.OptionParser(usage=usage)

optParser.add_option( "-i", "--input", type="string", dest="InputFile",
      default = "", help = "The file with gene ID that is to be annotated" )


(opts, args) = optParser.parse_args()

OutputFile = opts.InputFile.replace(".txt","-count.txt")

def main():
	with open (opts.InputFile,"r") as openInputFile, open (OutputFile,"w+") as openOutputFile:
		for line in openInputFile:
			ElementList = line.strip("\n").split("\t")
			TupleList=[] 
			if len(ElementList)<=2 or ElementList[1] =="0":
				continue
			elif ElementList[1] =="1":
				openOutputFile.write("%s\t%s\t%s\n" % (ElementList[0],ElementList[1],ElementList[2] ))
				continue
			else:
				NewList=ElementList[2].replace("[","").replace("]","").split(";")
				for element in NewList:
					stringlist=re.findall("\d+",element)
					RegionTuple=tuple([int(n) for n in stringlist])
					TupleList.append(RegionTuple)
				MergedList=merge_intervals(TupleList)
				openOutputFile.write("%s\t%s\t%s\n" % (ElementList[0],len(MergedList),";".join(map(str,MergedList)) ))
	stop = timeit.default_timer()
	print stop - start, "seconds. Done"
	

def merge_intervals(intervals):
    s = sorted(intervals, key=lambda t: t[0])
    m = 0
    for  t in s:
        if t[0] > s[m][1]:
            m += 1
            s[m] = t
        else:
            s[m] = (s[m][0], t[1])
    return s[:m+1]



if __name__ == "__main__":
   main()
