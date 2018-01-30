############################################################
#
# This code should take in a rule set, then play through a
# game of snake and return the score
#
############################################################

class Board():
    def __init__(self):
        # Initialize the snake. Place at random location
        # Make a coordinate grid
        # Add one fruit
        # TODO

    def gen_fruit(self):
        # After fruit is eaten, generate new one at unoccupied pos
        # TODO


class Snake():
    def __init__(self, x, y):
        # Give the snake the coords of its head
        self.head = (x,y)
        self.body = [(x, y)]
        self.score = 1  # Score is the length of snake at end

    def eat_fruit(self):
        # TODO 
    
    def get_neighborhood(self, board):
        # TODO
