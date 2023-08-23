#%%
from esop_opt import BF
from cube import Cube
from esop import ESOP
from input_string import BString
from helpers import *
from numpy import binary_repr, load, save
from numpy import array as nparray
from numpy import zeros as npzeros
from numpy import append as npappend
import numpy.linalg as nplinalg
import numpy as np
import os
from itertools import product as itproduct
# %%
table = load("cache/mtable_s108.npy")
# %%
key = 0
truth_table = table[key]
n = 16
# %%
bf = BF(n, truth_table)
# %%
matrix, Y = bf.make_solution_matrix()

# %%
len(bf)
# %%
