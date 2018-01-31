import numpy as np
import time

xRange = [0., 2.]
yRange = [0., 2.]
aRange = [0., 2.]
bRange = [0., 2.]

def z(xy): #function to optimize
    x = xy[0]
    y = xy[1]
    a = xy[2]
    b = xy[3]
    return np.sin(x)*np.sin(y)*np.sin(a)*np.sin(b)
    #return 7*x*y/(np.e**(x**2+y**2))

class PSO():
    def __init__(self, d, f, domain, pos = None, vel = None): #n = dimensions
        self.pos = pos
        self.domain = domain #assumes periodic boundary
        if self.pos == None:
            self.pos = np.zeros(d)
            for i in range(d):
                self.pos[i] = np.random.uniform(domain[i][0], domain[i][1]) #domain should be a 2D array of the upper and lower bounds for each dimension of the function
        self.vel = vel
        if self.vel == None:
            self.vel = np.zeros(d)#zero initial velocity has been shown to be the most effective method of velocity initialization
        self.best_pos = np.copy(self.pos)
        self.best = f(self.pos)
        self.func = f  # the function we want to optimize
    def step(self, gb, w, c1, c2):
        self.vel = w*self.vel + c1*np.random.random()*self.best_pos + c2*np.random.random()*gb
        self.pos += self.vel
        self.periodicBoundary()
        if self.func(self.pos) > self.best:
            self.best_pos = np.copy(self.pos)
            self.best = self.func(self.pos)
    def periodicBoundary(self):
        for i in range(len(self.pos)):
            L = self.domain[i][0]
            U = self.domain[i][1]
            if self.pos[i] < L:
                self.pos[i] += U - L
                self.pos[i] = self.pos[i] % (U-L)
            elif self.pos[i] > U:
                self.pos[i] += L - U
                self.pos[i] = self.pos[i] % (U-L)

def init(n):
    swarm = []
    for i in range(n):
        swarm.append(PSO(4, z, [xRange, yRange, aRange, bRange]))
    return swarm

swarm = init(100)
w = 0.98 #inertia parameter
c1 = 0.02 #personal best acceleration parameter
c2 = 0.04 #global best acceleration parameter
globalbest = -sys.float_info.max
globalbest_pos = None
for i in range(len(swarm)):
    if swarm[i].best > globalbest:
        globalbest = swarm[i].best
        globalbest_pos = swarm[i].best_pos
start = time.time()
tick = 0
while(globalbest < 0.999):
    for i in range(len(swarm)):
        swarm[i].step(globalbest_pos, w, c1, c2)
        if swarm[i].best > globalbest:
            globalbest = swarm[i].best
            globalbest_pos = swarm[i].best_pos
    tick += 1
print(globalbest, globalbest_pos, tick)
print(time.time() - start)