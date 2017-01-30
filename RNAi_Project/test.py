import numpy
import timeit;
start = timeit.default_timer()
import scipy.stats as stats
import sys, optparse
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
Rstats = importr('stats')


BinormalPvalue=stats.binom_test(40,121,0.0219928)
print BinormalPvalue