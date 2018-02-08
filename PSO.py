import numpy as np
import sys
import time
import random

xRange = [0., 2.]
yRange = [0., 2.]
aRange = [0., 2.]
bRange = [0., 2.]

def initGrid(d, n):
    grid = []
    grid.append([2]*d) #top wall
    for i in range(d-2):
        grid.append([0]*d)
        grid[i+1][0] = 2 #left wall
        grid[i+1][d-1] = 2 #right wall
    grid.append([2]*d) #bot wall
    while (n > 0): #add n cans
        a = random.randint(0, len(grid)-1)
        b = random.randint(0, len(grid)-1)
        if grid[a][b] == 0:
            grid[a][b] = 1
            n -= 1
    return grid

class PSO():
    def __init__(self, d, f, domain, pos = None, vel = None, robby=None): #n = dimensions
        self.pos = pos
        self.domain = domain #assumes periodic boundary
        if not np.any(self.pos):
            self.pos = np.zeros(d)
            for i in range(d):
                self.pos[i] = np.random.uniform(domain[i][0], domain[i][1]) #domain should be a 2D array of the upper and lower bounds for each dimension of the function
        self.vel = vel
        if self.vel == None:
            self.vel = np.zeros(d)#zero initial velocity has been shown to be the most effective method of velocity initialization
        self.best_pos = np.copy(self.pos)
        if not robby:
            self.best = f(self.pos)
            self.func = f  # the function we want to optimize
        else:
            score = self.score_pos(robby)
            self.best = score[0]
            self.strat = score[1]
            

    def score_pos(self, robby):
        U = []
        W = []
        V = []
        grid = initGrid(10, 40)
        for i in range(3):
            U.append(self.pos[5*i:5*(i+1)])
        for i in range(3):
            W.append(self.pos[3*i+15:3*(i+1)+15])
        for i in range(6):
            V.append(self.pos[3*i+24:3*(i+1)+24])
        U = np.array(U)
        W = np.array(W)
        V = np.array(V)
        score = robby.play_with_RNN(U, V, W, grid)
        return score

    def step(self, gb, w, c1, c2, robby=None):
        self.vel = w*self.vel + c1*np.random.random()*self.best_pos + c2*np.random.random()*gb
        self.pos += self.vel
        self.periodicBoundary()
        if not robby and self.func(self.pos) > self.best:
            self.best_pos = np.copy(self.pos)
            self.best = self.func(self.pos)
        if robby:
            # Put components of the position into synapses
            score = self.score_pos(robby)
            #print(score)
            if score[0] > self.best:
                self.best_pos = np.copy(self.pos)
                self.best = score[0]
                self.strat = score[1]


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

if __name__ == 'main':
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

"""Finished Epoch (score 214). Pos: [ 7.1672279   0.02993712 -2.66411889 -3.56642071  4.20449331 -0.16198682
  4.64522144 -1.2965104  -2.4643721   4.64137075  7.30523026  0.16399984
  0.02209856  0.36007386 -4.39863391 -4.60659643  1.88839538 -0.27271591
  0.23926015  4.17146198 -3.48052079 -3.07959852  2.42464044 -1.68055465
  0.28460891  2.47596972 -0.91486373 -3.88909078  2.78262337  7.43812095
 -2.05347992  5.662662    3.87528959  2.63361966  6.25318129  0.91008109
 -4.73042185 -1.93609789  3.48232229  8.5789724   3.94766857  4.45197993]"""