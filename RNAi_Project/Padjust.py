#!/usr/bin/python
import scipy.stats as stats
import sys, optparse
import timeit;
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
stats = importr('stats')