#%%
import cube
import esop
import helpers
import truthtable
import numpy as np
import networkx as nx
# %%
mtable = np.load("../ESOP2tmp/mtable_s108.npy")
# %%
len(mtable[0])
# %%
n = 8
length = 2*n
tt = truthtable.TruthTable(length, mtable[0])
# %%
tt.reduce_esop()
# %%
