import random
import sys
from RNN_basic import softmax, RNN
import numpy as np
from PSO import PSO, initGrid
import matplotlib.pyplot as plt

# TODO --> Get rid of print statements. IO is slow

class robot():
    def __init__(self, pos = None):
        if pos == None:
            self.pos = [1, 1]
        self.score = 0
        self.moves = [self.left, self.right, self.up, self.down, self.random, self.pickupCan]


    def reset(self):
        self.score = 0
        

    def left(self, grid):
        if grid[self.pos[0]-1][self.pos[1]] == 2:
            #print("Failed to move left")
            self.score -= 5
        else:
            self.pos[0] -= 1


    def right(self, grid):
        if grid[self.pos[0]+1][self.pos[1]] == 2:
            #print("Failed to move right")
            self.score -= 5
        else:
            self.pos[0] += 1

    
    def up(self, grid):
        if grid[self.pos[0]][self.pos[1]-1] == 2:
            #print("Failed to move up")
            self.score -= 5
        else:
            self.pos[1] -= 1


    def down(self, grid):
        if grid[self.pos[0]][self.pos[1]+1] == 2:
            #print("Failed to move down")
            self.score -= 5
        else:
            self.pos[1] += 1

            
    def random(self, grid):
        i = random.randint(1, 4)        
        if i == 1: self.left(grid)
        elif i == 2: self.right(grid)
        elif i == 3: self.up(grid)
        elif i == 4: self.down(grid)

            
    def pickupCan(self, grid):
        if grid[self.pos[0]][self.pos[1]] == 1:
            grid[self.pos[0]][self.pos[1]] = 0
            #print("Successfully picked up can")
            self.score += 10
        else:
            #print("Failed to pick up can")
            self.score -= 1

            
    def inputs(self, grid):
        middle = grid[self.pos[0]][self.pos[1]]
        left = grid[self.pos[0]-1][self.pos[1]]
        right = grid[self.pos[0]+1][self.pos[1]]
        down = grid[self.pos[0]][self.pos[1]-1]
        up = grid[self.pos[0]][self.pos[1]+1]
        return [middle, left, right, down, up]


    def play_with_RNN(self, U=None, V=None, W=None, grid=initGrid(10, 40)):
#        grid = [[elem for elem in self.grid[k]] for k in range(len(self.grid))]
        strat = RNN()
        if np.any(U) and np.any(V) and np.any(W):
            strat.U = U
            strat.V = V
            strat.W = W        
        for _ in range(100):
            input = np.array([self.inputs(grid)])
            out = strat.predict(input)[0]
            self.moves[out](grid)
        ret = self.score
        self.score = 0
        self.pos = [1, 1]
        return [ret, strat]

    def init_swarm(self, n, parameters=42):
        swarm = []
        dimension = parameters
        ranges = []
        for i in range(parameters):
            ranges.append([-5, 5])
        
        for i in range(n):
            swarm.append( PSO(parameters, lambda x: x, ranges, pos=np.random.uniform(-1, 1, parameters), robby=self) )
        return swarm


    def optimize(self): 
        swarm = self.init_swarm(100)
        w = .98
        c1 = .02
        c2 = .04
        bests = []
        averages = []
        global_best = -sys.float_info.max
        global_best_pos = None
        for i in range(len(swarm)):
            print(swarm[i].best)
            if swarm[i].best > global_best:
                global_best = swarm[i].best
                global_best_pos = swarm[i].best_pos
                global_best_strat = swarm[i].strat
        tick = 0
        while (tick <= 500):
            print("FINISHED ITERATION:", tick, global_best)
            if tick % 100 == 0:
                print("Finished Epoch. Pos:", global_best_pos)
                print("Strat: ", global_best_strat)
            for i in range(len(swarm)):
                swarm[i].step(global_best_pos, w, c1, c2, robby=self)
                if swarm[i].best > global_best:
                    global_best = swarm[i].best
                    global_best_pos = swarm[i].best_pos
                    global_best_strat = swarm[i].strat
            bests.append(global_best)
            average = 0
            for i in range(len(swarm)):
                average += swarm[i].best
            average /= len(swarm)
            averages.append(average)
            tick += 1
        self.strat = global_best_strat
        self.showRobby()
        plt.figure()
        ts = np.linspace(0, 500, 501)
        plt.plot(ts, bests)
        plt.title("Global best score over time")
        plt.figure()
        plt.plot(ts, averages)
        plt.title("Average score over time")
        return [global_best, global_best_pos] 
    
    def showRobby(self):
        pass

#grid = initGrid(10, 40)
#print(grid)
robby = robot()
robby.optimize()

print(robby.inputs(grid))