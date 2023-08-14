
#%%
import esop
import cube
from numpy import binary_repr
# %%
class TruthTable:

    def __init__(self, n, data):

        self.minterms, self.noterms, self.dontcares = self.process_data(n, data)

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
