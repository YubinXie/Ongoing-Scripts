import re;
import os;
import sys, optparse;
import timeit;

############Adjustbale Variables Explaination##############
#1. In Part1, you can edit the columns where you get your expression values are from by changing Expression_Average calculation in line37

#2. In Part2, you can edit the column number where your gene name is by changing GeneName definition in line55.
##########################################################

####################Initialization####################
start = timeit.default_timer()
usage="python GCTexpression_annotation.py GeneAnnotatedFile ExpressionDataFile OutputFile"
parser = optparse.OptionParser(usage=usage)
options, infile = parser.parse_args()
AnnotatedFile = infile[0]
ExpressionFile = infile[1]
OutputFile=infile[2]
OpenoutFile=open(OutputFile,"w+")
ExpressionDic={}
ExpressionAnnotation=[]
#######################################################

#################Part1 Take Gene Name and Value from Expression File####################
ExpressionRow=0
ExpressionGene=[]
with open(ExpressionFile,"r") as OpenExpressionFile:
  for row in OpenExpressionFile:
    ExpressionRow+=1
    #print ExpressionRow
    ElementList=row.split("\t")
    GeneName=ElementList[1]
    if ExpressionRow==1:
      Target=ElementList[32:34]
      print Target
    if ExpressionRow>1:
      Expression_Average= mean(Target)
      ExpressionDic[GeneName]=Expression_Average
      ExpressionGene.append(GeneName)
#print ExpressionGene 

###############################################################################

##################Part2 Give Variants Gene Expression Level##############################
AnnotatedFileLineNumber=0
RealAnnotatedFileLineNumber=0
with open(AnnotatedFile,"r") as OpenAnnotatedFile:
  for row in OpenAnnotatedFile:
    AnnotatedFileLineNumber+=1
    #print AnnotatedFileLineNumber
    if AnnotatedFileLineNumber==1:
      continue
    LineElementList=row.split(",")
    VariantInformation=("\t".join(LineElementList[1:5]))
    GeneName=LineElementList[6]
    GeneName=GeneName.replace('"',"")
    if GeneName in ExpressionGene:
      ExpressionLevel=ExpressionDic[GeneName]
      #ExpressionAnnotation.append(ExpressionLevel)
      RealAnnotatedFileLineNumber+=1
      #print GeneName, AnnotatedFileLineNumber
    else:
      ExpressionLevel="."

    if GeneName == ".":
        ExpressionLevel="."
    OpenoutFile.write("%s\t%s\t%s\n" % (VariantInformation,GeneName,ExpressionLevel))
#######################################################################################

##########End##############
OpenoutFile.close()
print "VariantsNumber=", AnnotatedFileLineNumber,"Annotated with Expression Data NUmber = ", RealAnnotatedFileLineNumber
stop = timeit.default_timer()
print "Total Running time= ",stop - start
############################