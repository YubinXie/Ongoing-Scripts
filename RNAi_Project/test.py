import rpy2
import scipy.stats as stats


Oddsratio, Pvalue = stats.fisher_exact([[2,15],[10,3]], alternative="less")
print Oddsratio, Pvalue