
#%%
import networkx as nx
import numpy as np
import string
from sympy.logic import SOPform
from sympy.logic.boolalg import to_anf
#from sympy.abc import a,b,c,d,e,f,g,h
from sympy.abc import *

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCXGate
#%%
def process_truth_table(table, value):

    """ take a table containing the  complete truth table excluding don't-cares
     and return a list of minterms and a list of dont-cares
       """
    
    minterms = np.array([], dtype=int)
    zeroterms = np.array([], dtype=int)
    n = table.shape[1] 

    for i in range(len(value)):

        entry = table[i]

        if value[i] == 1:
            minterms = np.append(minterms, int("".join([str(tt) for tt in entry]), 2))
        else:
            zeroterms = np.append(minterms, int("".join([str(tt) for tt in entry]), 2))
    
    dontcares = np.array([j for j in range(2**n) if (j not in minterms) and (j not in zeroterms)])


    # for entry in table:
    #     #print("".join([str(tt) for tt in entry]))
    #     if entry[-1] == 1:
    #         minterms = np.append(minterms, int("".join([str(tt) for tt in entry[:-1]]), 2))
    #     else:
    #         zeroterms = np.append(zeroterms, int("".join([str(tt) for tt in entry[:-1]]), 2))
    
    # dontcares = np.array([j for j in range(2**n) if (j not in minterms) and (j not in zeroterms)])

    return minterms, dontcares


def get_anf(table, value, symbols):

    minterms, dontcares = process_truth_table(table, value)
    minterms = [int(j) for j in minterms]
    dontcares = [int(j) for j in dontcares]
    sop = SOPform(symbols, minterms, dontcares)

    return sop.to_anf()

def pp_to_expression(n, pp_str):

    """ convert positive parity cube to B3 expression 
    """

    result = ["-"]*n
    pp_str = pp_str.replace("&", "")
    pp_str = pp_str.replace(" ", "")
    pp_str = pp_str.replace("(", "")
    pp_str = pp_str.replace(")", "")
    for c in pp_str:
        
        try:
            result[string.ascii_lowercase.index(c)] = "1"
        except:
            print("character causing a problem", c)
    
    return "".join(result)
# %%
# ttable = np.genfromtxt("../Finite-Group-QC/mult_r.csv", dtype=int, delimiter=",")
# ttable1 = ttable[:,:-1]
# myanf = get_anf(ttable1, [a,b,c,d,e,f,g,h])
# %%
class Cube:

    def __init__(self, expression):

        """ instantiate the cube class
          int n: lenght of the cube
          string expression: B3 string
          B3 = {0,1,-}  -> negative, positive and don't care
          """
        
        self.expression = expression
    

    def weight(self):

        return sum(self.expression[c] != "-" \
                   for c in range(len(self.expression)))


    def distance(self, other):

        assert len(self.expression) == len(other.expression)

        return sum(self.expression[c] != other.expression[c] \
                    for c in range(len(self.expression)))
    
    def xor_combine(self, other):

        combination_map = {"01":"-", "10":"-", \
                           "0-":"1", "-0":"1", \
                            "1-":"0", "-1":"0"}

        assert len(self.expression) == len(other.expression)
        assert self.distance(other) == 1

        new_expression = ""

        for i in range(len(self.expression)):

            if self.expression[i] != other.expression[i]:

                a = self.expression[i]
                b = other.expression[i]

                try:
                    new_expression += str(combination_map[f"{a}{b}"])
                except:
                    print("Weird in the combination")
                    return

            
            else:
                new_expression += self.expression[i]
        
        return Cube(new_expression)
    
    def toffoli_gate(self, labels = None, anc_label = None):
        """ convert the cube to a multi-controlled not gate also called Tofolli gate 
        """
        if labels is None:
            labels = 'q'
        if anc_label is None:
            anc_label = 'anc'

        qr = QuantumRegister(len(self.expression), labels)
        anc = QuantumRegister(1, anc_label)
        qc = QuantumCircuit(qr, anc)
        

        cares = []
        negatives = []
        for i in range(len(self.expression)):

            if self.expression[i] == "0":
                qc.x(qr[i])
                cares.append(i)
                negatives.append(i)
            
            if self.expression[i] == "1":
                cares.append(i)
        
        gate = MCXGate(len(cares))
        qc.append(gate, cares + [len(self.expression)])
        for neg in negatives:
            qc.x(neg)

        return qc  

    def __str__(self):

        result = ""
        for i in range(len(self.expression)):

            if self.expression[i] == "0":

                result += "~" + string.ascii_lowercase[i] 
            
            if self.expression[i] == "1":

                result += f"{string.ascii_lowercase[i]}"
        
        return result
            
#%%
def make_combination_graph(cubes):

    # figure out the edges
    edges = []
    for i in range(len(cubes)):
        for j in range(i, len(cubes)):
            try:
                c1 = cubes[i]
                c2 = cubes[j]
            except:
                print("issue in making graph", i,j, cubes)
            if c1.distance(c2) == 1:
                weight = (c1.xor_combine(c2)).weight()
                edges.append((c1, c2, weight))
    
    # make graph
    G = nx.Graph()
    G.add_nodes_from(cubes)
    G.add_weighted_edges_from(edges)

    return G

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
        
        
        if tmp_weight < weight:
            min_edge = (a,b)
            weight = tmp_weight
    
    c1,c2 = min_edge
    
    return min_edge



def process_cubes(cubes):

    """ Get the initial expressions of cubes 
    simplify by a greedy algorithm --> Among all the pairs of cubes that
    can be combined, combine those that result in a cube with lowest weights (among all
    the possible results)
    """

    G = make_combination_graph(cubes)

    # while there is an edge, reduce
    while G.number_of_edges() > 0:

        # get the pair to combine and create the combination
        n1, n2 = select_pair(G)
        new_node = n1.xor_combine(n2)
        #print(n1, n2, new_node)

        # remove each node in the pair
        G.remove_node(n1)
        G.remove_node(n2)

        #add the new node
        G.add_node(new_node)

        # add the new node and all the weighted edges if any
        new_edges = [(new_node, n, (new_node.xor_combine(n)).weight()) \
                      for n in G.nodes() if new_node.distance(n) == 1]

        G.add_weighted_edges_from(new_edges)
    
    return G

# %%
#%%
# Testing
# n = 8
# strform = myanf.__str__()
# strform = strform.split("^")
# expressions = [pp_to_expression(n, entry) for entry in strform]
# cubes = [Cube(expression) for expression in expressions]
# G = make_combination_graph(cubes)
# nx.draw(G)
# # %%
# GG = process_cubes(cubes)
# # %%
# nx.draw(GG)
# # %%
# for p in GG.nodes():
#     print(p)
# # %%
# p.toffoli_gate('q', 'anc').draw()
# # %%
# len(list(G.nodes()))
# # %%
# list(GG.nodes())[0].toffoli_gate().draw()
# # %%
# list(GG.nodes())[1].toffoli_gate().draw()

# %%
