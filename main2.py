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
minterms = tt.minterms
# %%
myesop = esop.ESOP(tt.minterms)

# %%
G = myesop.reduce()
# %%
for node in G.nodes:
    print(node.expression)
# %%
nx.draw(G)
# %%
for dc in tt.dontcares:
    print(dc.expression)
# %%
for node in G.nodes:
    for dc in tt.dontcares:
        if node.distance(dc) == 1:
            print(node, dc)
# %%
