
#%%
from esop import ESOP
import cube
from numpy import binary_repr
import networkx as nx
from itertools import product as itproduct
# %%
class TruthTable:

    def __init__(self, n, data):

        self.minterms, self.noterms, self.dontcares = self.process_data(n, data)
        self.n = n

    def process_data(self, n, data):

        assert len(data) == 2**n
        minterms = []
        dontcares = []
        noterms = []

        for i in range(2**n):

            if data[i] == "1":
                minterms.append(cube.Cube(binary_repr(i, n)))
            elif data[i] == "0":
                noterms.append(cube.Cube(binary_repr(i, n)))
            else:
                dontcares.append(cube.Cube(binary_repr(i, n)))
        
        return minterms,noterms, dontcares
    

#%%
# for i in itproduct(["0","1","-"], repeat=16):
#     print("".join(list(i)))
# %%
# import numpy as np
# np.save("cache/cubes16.npy",np.array([cube.Cube("".join(list(i))) for i in itproduct(["0","1","-"], repeat=16)]))
# %%
