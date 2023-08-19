# Author: Edison Murairi
# Data: August 12th, 2023
# Implement the Algebraic Normal Form Class
#%%
from cube import Cube
import networkx as nx
import helpers
# %%
class ESOP:

    def __init__(self, data):
        """ Take either a list of cubes or a string as explained below

        If a string, the string will contain the parities of each cube. The cubes are separated by a space
        Example: anf_str = '11--- --01-'
        Stor the anf as a list of cubes in the attribute cubes.
        """
        if isinstance(data, str):  
            self.cubes = [Cube(item) for item in data.split(" ")]
        
        else:
            self.cubes = data
    
    def evaluate(self, input):

        return sum(cube.evaluate_input(input) for cube in self.cubes) % 2
    
    def cost(self):

        return sum(cube.weight() for cube in self.cubes)
            
    
    def remove_duplicate_pairs(self):

        seen = {} # key expression -> value cube
        for cube in self.cubes:
            if not cube.expression in seen:
                seen[cube.expression] = cube
            
            else:
                del seen[cube.expression]
        
        self.cubes = [cube for _,cube in seen.items()]
    
    def add_esops(self, *others):

        cubes = [cube for cube in self.cubes]
        for other in others:
            cubes += other.cubes
        
        new_esop = ESOP(cubes)
        new_esop.remove_duplicate_pairs()

        return new_esop

    def combination_graph(self):
        """ make a weighted graph where each cube is a node. 
        There is an edge between two nodes if and only if the cubes can be combined: they have distance 1
        The weight of each edge is the weight of the combined cube if the cubes were combined.
        """

        G = nx.Graph()
        for i in range(len(self.cubes)):

            c1 = self.cubes[i]
            G.add_node(c1)

            for j in range(i+1, len(self.cubes)):

                c2 = self.cubes[j]
                G.add_node(c2)

                if c1.distance(c2) == 1:

                    G.add_edge(c1, c2)

        # # figure out the edges
        # edges = []
        # for i in range(len(self.cubes)):
        #     for j in range(i, len(self.cubes)):
        #         try:
        #             c1 = self.cubes[i]
        #             c2 = self.cubes[j]
        #         except:
        #             print("issue in making graph", i,j, self.cubes)
        #         if c1.distance(c2) == 1:
        #             #weight = (c1.xor_combine(c2)).weight()
        #             weight = 1
        #             edges.append((c1, c2, weight))
        
        # # make graph
        # G = nx.Graph()
        # G.add_nodes_from(self.cubes)
        # G.add_weighted_edges_from(edges)

        return G

    def reduce(self):

        """ Get the initial expressions of cubes 
        simplify by a greedy algorithm --> Among all the pairs of cubes that
        can be combined, combine those that result in a cube with lowest weights (among all
        the possible results)
        """

        G = self.combination_graph()

        # while there is an edge, reduce
        while G.number_of_edges() > 0:

            # get the pair to combine and create the combination
            #n1, n2 = helpers.select_pair(G)
            #new_node = n1.xor_combine(n2)

            n1, n2 = list(G.edges)[0]
            new_node = n1.xor_combine(n2)
            #print(n1, n2, new_node)

            # remove each node in the pair
            G.remove_node(n1)
            G.remove_node(n2)

            #add the new node
            G.add_node(new_node)

            # add all new edges
            for node in G.nodes():
                if new_node.distance(node) == 1:
                    G.add_edge(new_node, node)

            # add the new node and all the weighted edges if any
            # new_edges = [(new_node, n, (new_node.xor_combine(n)).weight()) \
            #             for n in G.nodes() if new_node.distance(n) == 1]

            # G.add_weighted_edges_from(new_edges)
        
        return list(G.nodes())

    def __len__(self):

        return len(self.cubes)
# %%
class ANF(ESOP):

    def __init__(self, anf_str):

        ESOP.__init__(anf_str)
# %%
# esop = ESOP("---- 1--- 1100 1110")
# G = esop.combination_graph()
# pos = {list(G.nodes)[i]:(i,i) for i in range(len(list(G.nodes)))}
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw(G)
# %%
cb1 = Cube("1110")
cb2 = Cube("0-1-")
cb3 = Cube("-011")
cb4 = Cube("1101")
cb5 = Cube("1-00")
esop1 = ESOP(cb1.expansion())
esop2 = ESOP(cb2.expansion())
esop3 = ESOP(cb3.expansion())
esop4 = ESOP(cb4.expansion())
esop5 = ESOP(cb4.expansion())
total = esop1.add_esops(esop2, esop3, esop4, esop5)
# %%
# for cube in esop1.cubes:
#     print(cube)
# # %%
# for cube in esop2.cubes:
#     print(cube)
# # %%
# for cube in total.cubes:
#     print(cube)
# # %%
# nx.draw(total.combination_graph())
# # %%
# G = total.reduce()
# # %%
# nx.draw(G)
# # %%
# for node in G.nodes():
#     print(node)
# # %%
# cb1 = Cube("110")
# cb2 = Cube("0-1")
# total = ESOP(cb1.expansion()).add_esops(ESOP(cb2.expansion()))
# nx.draw(total.combination_graph())
# # %%
# for cube in total.cubes:
#     print(cube)
# # %%
# nx.draw(total.reduce())
# # %%
# for node in total.reduce().nodes():
#     print(node)
# %%
