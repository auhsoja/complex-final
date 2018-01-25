import numpy as np
import sys

xRange = [-2., 2.]
yRange = [-2., 2.]

def z(xy):
    x = xy[0]
    y = xy[1]
    return 7*x*y/(np.e**(x**2+y**2))

class PSO():
    def __init__(self, n, f, domain, pos = None, vel = None): #n = dimensions
        self.pos = pos
        if self.pos == None:
            self.pos = []
            for i in range(n):
                self.pos.append(np.random.uniform(domain[i][0], domain[i][1])) #domain should be a 2D array of the upper and lower bounds for each dimension of the function
        self.vel = vel
        if self.vel == None:
            self.vel = [0.]*n #zero initial velocity has been shown to be the most effective method of velocity initialization
        self.best_pos = self.pos
        self.best = f(self.pos)
        
def master():
    swarm = init(10)
    w = 0.98 #inertia parameter
    c1 = 0.02 #personal best acceleration parameter
    c2 = 0.04 #global best acceleration parameter
    globalbest_pos = None
    globalbest = -sys.float_info.max
    for i in range(len(swarm)):
        if swarm[i].best > globalbest:
            globalbest = swarm[i].best
            globalbest_pos = swarm[i].best_pos

def init(n):
    swarm = []
    for i in range(n):
        swarm.append(PSO(2, z, [xRange, yRange]))
    return swarm
