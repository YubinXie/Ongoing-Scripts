import numpy
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

from fisher import pvalue

Rstats = importr('stats')

P=pvalue(8,0,26543934,25102846)
print P.two_tail
#Yuwen used two_tail
BinormalPvalue=stats.binom_test(40,121,0.0219928)
#print BinormalPvalue

