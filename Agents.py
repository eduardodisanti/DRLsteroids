import math
import random
from collections import defaultdict

import numpy as np

class SARSAAgent:

    def __init__(self, shape, x, y, nA=2):

        self.shape = shape
        self.x = x
        self.y = y

        self.nA = nA
        self.Q = defaultdict(lambda: np.zeros(self.nA))
        self.epsilon = 1
        self.gamma = 0.75
        self.alpha = 0.3
        self.i_episode = 0
        self.epsilon_decay = 0.88
        self.epsilon_min = 0.00000001


    def select_action(self, state):
        """ Given the state, select an action.

        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space USING EPSILON-GREEDY
        """

        if random.random() < self.epsilon:  # select greedy action with probability epsilon
            return np.argmax(self.Q[state])
        else:  # otherwise, select an action randomly
            return random.choice(np.arange(self.nA))

        return action

    def get_ship(self):

        return(self.shape, self.x, self.y)


#    def get_random_action(self):

#        return np.sign(1 / (1 + math.exp(-random.randrange(-1,2))) - 0.5)


#    def act(self, state):


#        return self.get_random_action()


    def update_Q(self, state, action, reward, next_state):
        current = self.Q[state][action]
        Qsa_next = np.max(self.Q[next_state]) if next_state is not None else 0  # value of next state
        target = reward + (self.gamma * Qsa_next)
        new_value = current + (self.alpha * (target - current))
        return new_value


    def step(self, state, action, reward, next_state, done):
        """ Update the agent's knowledge, using the most recently sampled tuple.

        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """

        self.i_episode += 1
        self.epsilon = self.epsilon + self.epsilon_decay  # eps value and decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min

        if done == False:
            #            action = self.select_action(state)         # epsilon-greedy action selection
            #            next_state, reward, done, info = self.env.step(action)  # take action A, observe R, S'
            self.Q[state][action] = self.update_Q(state, action, reward, next_state)

