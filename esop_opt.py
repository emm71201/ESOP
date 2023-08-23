# implement an esop optimization strategy by brute forcing
#%%
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


import galois
GF = galois.GF(2)
#%%
class BF:

    
    def __init__(self, n, ttable):
        """ take the truth table as a string of length 2^n 
        The string contains 0, 1, - (- means don't-care)
        """

        assert len(ttable) == 2**n
        self.length = 2**n
        self.n = n
        self.data = ttable
        self.odds, self.evens = self.get_even_odd()
        self.cubemap = self.get_cubes()
        self.evens_neighborhoods = self.get_neighborhoods(self.evens)
        self.odds_neighborhoods = self.get_neighborhoods(self.odds)
    
    
    def __len__(self):

        return self.length
    
    
    def get_even_odd(self):

        evens = []
        odds = []

        for i in range(len(self)):
            ch = self.data[i]
            if ch == "0":
                evens.append(i)
            if ch == "1":
                odds.append(i)
        
        return odds, evens
    
    
    def get_cubes(self):

        return make_cubes_map(self.n)
    
    
    def get_neighborhoods(self, nodes):

        result = {}
        for node in nodes:
            brepr = binary_repr(node, self.n)
            bstring = BString(brepr)
            result[node] = bstring.covering()
        
        return result
    

    
    def mapvector(self, cubeset):

        result = GF.Zeros(shape=3**self.n)

        for cube in cubeset:

            result[self.cubemap[cube]] = 1
        
        return result
    
    
    def make_solution_matrix(self):

        """ form the equation matrix * c = y"""

        matrix = []
        Y = []

        for even, ngb in self.evens_neighborhoods.items():

            vect = self.mapvector(ngb)
            vect = npappend(vect, 0)
            #Y.append(0)

            matrix.append(vect)

        
        for odd, ngb in self.odds_neighborhoods.items():

            vect = self.mapvector(ngb)
            vect = npappend(vect, 1)
            #Y.append(1)

            matrix.append(vect)

        
        return GF(matrix), GF(Y)
    
    
    def valiate_esop(self, esop):

        for i in range(len(self)):

            if self.data[i] != "-":

                brepr = binary_repr(i, self.n)

                if esop.evaluate(brepr) != int(self.data[i]):

                    return False

        return True
#%%
# try on BT
# n = 10
# ttable = load("cache/BT_Table.npy")
# bf = BF(n, ttable[4])
# matrix, Y = bf.make_solution_matrix()
# nspace = matrix.null_space()
# #nspace = load("cache/nspace_BT_0.npy")
# #%%
# cubemap = bf.cubemap
# all_cubes_list = list(cubemap.keys())
# # %%
# bestesop = None
# bestcost = np.inf
# for nvect in nspace:
#     if nvect[-1] == 1:
#         coordinates = np.where(nvect[:-1] == 1)[0]
#         cubes_list= []
#         for c in coordinates:
#             cubes_list.append(Cube(all_cubes_list[c]))
        
#         myesop = ESOP(cubes_list)
#         print("Starting reduction")
#         reduced = ESOP(myesop.reduce())
#         if reduced.cost() < bestcost:
#             bestesop = reduced
#             bestcost = len(reduced)
#         #print(f"Number of terms {len(reduced)}")
#         # for cubered in reduced:
#         #     print(cubered)
#         print("------------")
# # %%
# np.save("cache/nspace_BT_4.npy", nspace)
# # %%
# for cube in bestesop.cubes:
#     print(cube)
# # %%
# bf.valiate_esop(bestesop)
# # %%
# np.save("BT_bestesop_4.npy", bestesop)
# # %%
# bestesop.cost()
# # %%
# len(bestesop)
# # %%
