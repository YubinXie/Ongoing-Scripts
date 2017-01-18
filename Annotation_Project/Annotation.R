library(splitstackshape)
annotate1.data <- read.csv(file='~/tools/annovar/MIdataSplit.hg19_multianno.csv')[,c(1:27,39:40)]
annotate2.data <- read.csv(file='~/tools/annovar/MIdataSplitAv.hg19_multianno.csv')[,6]
count.case <- read.csv(file='~/tools/annovar/MIGen_Case_Split_Count.frq.count',sep = "\t", header = FALSE)[-1,]
count.control <- read.csv(file='~/tools/annovar/MIGen_Control_Split_Count.frq.count',sep = "\t", header = FALSE)[-1,]
count.case <- cSplit(indt =count.case, splitCols = "V6", sep=":",drop = TRUE)
count.control <- cSplit(indt=count.control, splitCols = "V6", sep=":",drop = TRUE)
annotate.data <- cbind(annotate1.data[,1:5],annotate2.data,count.case[,4], count.case[,7],count.control[,7],annotate1.data[,6:29])
colnames(annotate.data)[6]<-"avsnp147"
colnames(annotate.data)[7]<-"Chr_Num"
colnames(annotate.data)[8]<-"Case_Num"
colnames(annotate.data)[9]<-"Control_Num"
exonconstarinscore.missense.data <-read.csv(file='~/tools/annovar/mySPlitMIdata.avinput.hg19_multianno.txt',sep = "\t")[,6]
exonconstarinscore.missense.data <-gsub("Name=","",exonconstarinscore.missense.data)
annotate.data <- cbind(annotate.data,exonconstarinscore.missense.data)
colnames(annotate.data)[33]<-"ExonConScore_Missense"
save(annotate.data,file="~/R/Annotation/MIdataAnnotationV3")
