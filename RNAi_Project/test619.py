import timeit;
start = timeit.default_timer()
import sys, optparse
import re
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from rpy2.robjects.packages import importr

x=[0]*101146 + [1]*2