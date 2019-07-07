import math
import random
import numpy as np

class Agent:

    def __init__(self, shape, x, y):

        self.shape = shape
        self.x = x
        self.y = y


    def get_ship(self):

        return(self.shape, self.x, self.y)


    def get_random_action(self):

        return np.sign(1 / (1 + math.exp(-random.randrange(-1,2))) - 0.5)


    def act(self, state):

        return self.get_random_action()
