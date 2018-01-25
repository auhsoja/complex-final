import numpy as np

xRange = [0, 1]
yRange = [0, 1]

def f(x, y):
    return np.e**(x-y) + np.sin(x*y)

class PSO():
    def __init__(self, n = 1, pos = None, vel = None):
        self.pos = pos
        if self.pos == None:
            self.pos = np.random.rand(n)
        self.vel = vel
        if self.vel == None:
            self.vel = np.random.rand(n)

swarm = []
for i in range(10):
    swarm.append(PSO(2))
    print(swarm[i].pos)