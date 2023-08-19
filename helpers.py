# Author: Edison Murairi
# Date: August 12th, 2023
# Build helper functions
#%%
import string
from itertools import product as itproduct
import os
from numpy import save, load
#%%
def ANF_from_alphabetical(nbits, anf_str):
    """ 
    int nbits: The numbe rof bits
    string example from alphabetical form: a & b ^ ~c & d representing the Algebraic Normal Form (ANF)
    return the string in B3 = {0,1,-} form. 
    Example:
    nbits = 4
    input a & b ^ ~c & d
    return 11-- --01
    """

    anf_str =anf_str.replace(" ", "")
    result = ""
    ii = 0
    while ii < len(anf_str):

        tmp = ["-"]*nbits
        parity = "1" # positive 
        while ii < len(anf_str) and anf_str[ii] != "^":
            if anf_str[ii] == "~":
                parity = "0" # negative
            
            elif anf_str[ii] == "&":
                pass
            
            else:
                ch = anf_str[ii]
                indx = string.ascii_lowercase.index(ch)
                if indx >= nbits:
                    print("We assume that the variables are chosen in order from the alphabet")
                    return
                tmp[indx] = parity
                parity = "1"
            
            ii += 1
        
        result += "".join(tmp) + " "

        ii += 1
    
    if result[-1] == " ":
        result = result[:-1]
    
    return result

def select_pair(G):

    """ input : networkx graph"""

    weight = None
    min_edge = None
    for edge in G.edges:

        a,b = edge
        tmp_weight = G[a][b]['weight']

        if weight is None and min_edge is None:
            min_edge = (a,b)
            weight = tmp_weight
        
        
        if tmp_weight > weight:
            min_edge = (a,b)
            weight = tmp_weight
    
    c1,c2 = min_edge
    
    return min_edge

def make_cubes_map(n):

    fname = os.path.join("cache", f"cubes_{n}.npy")
    cubemap = {}

    if os.path.exists(fname):

        cubemap = load(fname, allow_pickle=True).item()
    
    else:
        indx = 0
        for cube in itproduct(["-", "1", "0"], repeat=n):

            cubemap["".join(list(cube))] = indx

            indx += 1

        save(fname, cubemap)
    
    return cubemap
# %%
cubes = make_cubes_map(10)
# %%
cubes
# %%
