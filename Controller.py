import time

from Environments import Environment
from Scenarios import Scenario
from dqn_agents import Agent
import matplotlib.pyplot as plt

class Controller:

    def __init__(self, scenario, environment, agent, eps=1, eps_decay=0.95, eps_min=0.001):

        self.action_map = (-1,0,1)
        self.scenario = scenario
        self.graphic_w = self.scenario.width
        self.graphic_h = self.scenario.height
        self.speed = 0.25
        self.scene = scenario
        self.agent = agent
        self.bangs = 0
        self.epsilon = eps
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.episodes = 0
        self.max_score = -999999

        self.environment = environment
        #self.ship = Ship()

    def draw_scenario(self):
        print("\033[H\033[J")
        print("Score", self.scenario.score, "steps", self.environment.steps, "episodes", self.episodes, "max", self.max_score)
        self.scenario.print_scenario()

    def game_loop(self, episodes=100, train=False):

        actions_dist = {-1:0, 0:0, 1:0}
        scores = []
        rewards = []
        for e in range(episodes):
            self.environment.reset()
            self.episodes = e
            self.scenario.score = 0
            while not self.environment.done:
                self.scenario.put_ship(self.agent.get_ship())
                self.draw_scenario()

                state = self.scenario.create_state(self.scenario.board)
                action = self.agent.act(state, self.epsilon)
    #            act = self.agent.act(self.scenario)
    #	     agent performs the selected action

                actions_dist[(action - 1)]+=1
                self.agent.x += (action - 1)
                if self.agent.x < 0:
                    self.agent.x = 0
                elif self.agent.x > self.scenario.width - 1:
                    self.agent.x = self.scenario.width - 1

                next_state, reward, done, _ = self.environment.step(action)
                # agent performs internal updates based on sampled experience
                if not done:
                    next_state = self.scenario.create_state(next_state)
                    self.agent.step(state, action, reward, next_state, done)
                    self.environment.step(action=action)
                    if not train:
                        time.sleep(self.speed)

            self.environment.reset()
            #self.scenario.move_down_scenario(1)

            self.epsilon*=self.eps_decay
            if self.epsilon < self.eps_min:
                self.epsilon = self.eps_min
            if self.max_score < self.scenario.score:
                self.max_score = self.scenario.score
            if self.episodes % 2 == 0:
                scores.append(self.scenario.score)
                plt.plot(scores, ".", color="b", label="Score")
                plt.title("episodes " + str(self.episodes) + " eps "+str(self.epsilon) + " score " + str(self.scenario.score))
                plt.pause(0.1)

        #plt.plot(rewards, label="Reward")
        plt.show()
        print(actions_dist)

SHAPE_1 = "A"
EPS_START = 1           # START EXPLORING A LOT
GAMMA = 0.99            # discount factor - THE OBJECTIVE OF THE GAME IS TO MAXIMIZE REWARDS AT THE END, HAS TO BE HIGH

BUFFER_SIZE = int(1e5)  # replay buffer size
BATCH_SIZE = 64         # minibatch size
TAU = 1e-3              # for soft update of target parameters
LR = 5e-4               # learning rate
UPDATE_EVERY = 4        # how often to update the network
action_size = 3         # -1 LEFT, 0 STAY, 1 RIGHT

s = Scenario((SHAPE_1, 1, 20), size=(40, 20), density=10)

state_size = s.width * s.height + 1
a = Agent((SHAPE_1, 1, 20), state_size=state_size, action_size=action_size, seed=0, gamma=GAMMA, buffer_size=BUFFER_SIZE, batch_size=BATCH_SIZE, tau=TAU, lr=LR, update_every=UPDATE_EVERY)
e = Environment(s, max=1000)
c = Controller(s, e, a)
c.game_loop(episodes=10000, train=True)
