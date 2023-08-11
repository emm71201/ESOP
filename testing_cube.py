#%%
from cube import Cube
import random
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
