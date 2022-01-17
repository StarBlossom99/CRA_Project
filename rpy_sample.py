import rpy2.robjects as robjects
import rpy2
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages




base = importr('base')
utils = rpackages.importr('utils')

utils. chooseCRANmirror(ind=1)

packnames = ('ggplot2', 'hexbin')

from rpy2.robjects.vectors import StrVector

names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) >0:
    utils.install_packages(StrVector(names_to_install))


pi = robjects.r['pi']
print(pi[0])





