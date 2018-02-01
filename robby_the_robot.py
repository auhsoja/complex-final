import random

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

class robot():
    def __init__(self, grid, pos = None):
        if pos == None:
            self.pos = [random.randint(1, len(grid)-2), random.randint(1, len(grid)-2)]
        self.score = 0
        
    def left(self, grid):
        if grid[self.pos[0]-1][self.pos[1]] == 2:
            print("Failed to move left")
            self.score -= 5
        else:
            self.pos[0] -= 1

    def right(self, grid):
        if grid[self.pos[0]+1][self.pos[1]] == 2:
            print("Failed to move right")
            self.score -= 5
        else:
            self.pos[0] += 1
    
    def up(self, grid):
        if grid[self.pos[0]][self.pos[1]-1] == 2:
            print("Failed to move up")
            self.score -= 5
        else:
            self.pos[1] -= 1

    def down(self, grid):
        if grid[self.pos[0]][self.pos[1]+1] == 2:
            print("Failed to move down")
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
            print("Successfully picked up can")
            self.score += 10
        else:
            print("Failed to pick up can")
            self.score -= 1
            
    def inputs(self, grid):
        middle = grid[self.pos[0]][self.pos[1]]
        left = grid[self.pos[0]-1][self.pos[1]]
        right = grid[self.pos[0]+1][self.pos[1]]
        down = grid[self.pos[0]][self.pos[1]-1]
        up = grid[self.pos[0]][self.pos[1]+1]
        return [middle, left, right, down, up]

grid = initGrid(5, 1)
print(grid)
robby = robot(grid)
print(robby.inputs(grid))