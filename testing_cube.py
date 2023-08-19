#%%
from cube import Cube
import random
import numpy
# %%
# initialize cubes randomly and check the string output
# print the weight of each cube as well
b3 = ["0", "1", "-"]
ncubes = 15
length = 10
for i in range(ncubes):
    expr = "".join([random.choice(b3) for j in range(length)])
    mycube = Cube(expr)
    print(expr, "\t", mycube, "\t", mycube.weight())
# %%
# initialize cubes randomly and compute the distances
b3 = ["0", "1", "-"]
ncubes = 10
length = 5
cubes = [Cube("".join([random.choice(b3) for j in range(length)])) for j in range(ncubes)]
for i in range(len(cubes)):
    for j in range(i, len(cubes)):
        print(cubes[i], "\t", cubes[j], "\t", cubes[i].distance(cubes[j]))
# %%
cubes[0].toffoli_gate().draw()
# %%
# Testing the expansion
exp = "10-11"
cube = Cube(exp)
for cc in cube.expansion():
    print(cc)
# %%
print(cube)
# %%
cube.evaluate_input("-1-")
# %%
cube = Cube("1011-01--1010-1-")
mt, nt = cube.minterms_noterms()
# %%
len(mt) + len(nt)
# %%
numpy.log(len(mt) + len(nt))/numpy.log(2)
# %%
c1 = Cube("110")
c2 = Cube("111")
# %%
print(c1.xor_combine(c2))
# %%
