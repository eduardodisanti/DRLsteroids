import time

from Environments import Environment
from Scenarios import Scenario
from dqn_agents import Agent
import matplotlib.pyplot as plt

class Controller:

    def __init__(self, scenario, environment, agent, eps=1, eps_decay=0.9995, eps_min=0.001):

        self.action_map = (-1,0,1)
        self.scenario = scenario
        self.graphic_w = self.scenario.width
        self.graphic_h = self.scenario.height
        self.speed = 0.1
        self.scene = scenario
        self.agent = agent
        self.score = 0
        self.bangs = 0
        self.epsilon = eps
        self.eps_decay = eps_decay
        self.eps_min = eps_min

        self.environment = environment
        #self.ship = Ship()

    def draw_scenario(self):
        print("\033[H\033[J")
        print("Score", self.score)
        self.scenario.print_scenario()

    def game_loop(self, episodes=100, train=False):

        scores = []
        for e in range(episodes):

            while not self.environment.done:
                bang = self.scenario.put_ship(self.agent.get_ship())
                if bang:
                    self.score -=10
                    self.bangs += 1
                self.draw_scenario()

                _action = self.agent.act(self.scenario.board, self.epsilon)
    #            act = self.agent.act(self.scenario)
    #	     agent performs the selected action

                action = self.action_map[_action]
                self.agent.x += action
                if self.agent.x < 0:
                    self.agent.x = 0
                elif self.agent.x > self.scenario.width:
                    self.agent.x = self.scenario.width

                next_state, reward, done, _ = self.environment.step(action)
                # agent performs internal updates based on sampled experience
                if not done:
                    self.agent.step(self.scenario.board, action, reward, next_state, done)

                    self.environment.step(action=action)
                    time.sleep(self.speed)
                #self.scenario.move_down_scenario(1)
            scores.append(self.scenario.score)
            self.environment.reset(s)
            self.epsilon*=self.eps_decay
            if self.epsilon < self.eps_min:
                self.epsilon = self.eps_min


        plt.plot(scores)
        plt.show()
SHAPE_1 = "A"
EPS_START = 1           # START EXPLORING A LOT
GAMMA = 0.99            # discount factor - THE OBJECTIVE OF THE GAME IS TO MAXIMIZE REWARDS AT THE END, HAS TO BE HIGH

BUFFER_SIZE = int(1e5)  # replay buffer size
BATCH_SIZE = 64         # minibatch size
TAU = 1e-3              # for soft update of target parameters
LR = 5e-4               # learning rate
UPDATE_EVERY = 4        # how often to update the network
action_size = 3         # -1 LEFT, 0 STAY, 1 RIGTH

s = Scenario((SHAPE_1, 10, 10), size=(20, 20), density=5)

state_size = s.width * s.height
a = Agent((SHAPE_1, 10, 20), state_size=state_size, action_size=action_size, seed=0, gamma=GAMMA, buffer_size=BUFFER_SIZE, batch_size=BATCH_SIZE, tau=TAU, lr=LR, update_every=UPDATE_EVERY)
e = Environment(s, max=1000)
c = Controller(s, e, a)
c.game_loop()
