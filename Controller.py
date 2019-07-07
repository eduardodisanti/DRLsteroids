import time

from Agents import Agent
from Environments import Environment
from Scenarios import Scenario


class Controller:

    def __init__(self, scenario, environment, agent):

        self.scenario = scenario
        self.graphic_w = self.scenario.width
        self.graphic_h = self.scenario.height
        self.speed = 0.1
        self.scene = scenario
        self.agent = agent
        self.score = 0
        self.bangs = 0

        self.environment = environment
        #self.ship = Ship()

    def draw_scenario(self):
        print("\033[H\033[J")
        print("Score", self.score)
        self.scenario.print_scenario()


    def game_loop(self):

        while not self.environment.done:
            bang = self.scenario.put_ship(self.agent.get_ship())
            if bang:
                self.score -=10
                self.bangs += 1
            self.draw_scenario()

            act = self.agent.act(self.scenario)

            self.agent.x += act
            if self.agent.x < 0:
                self.agent.x = 0
            elif self.agent.x > self.scenario.width:
                self.agent.x = self.scenario.width

            self.environment.step(action=act)
            time.sleep(self.speed)
            self.scenario.move_down_scenario(1)

SHAPE_1 = "A"
a = Agent(SHAPE_1, 10, 20)
s = Scenario((SHAPE_1, 10, 10), size=(20, 20), density=5)
e = Environment(s, max=1000)
c = Controller(s, e, a)
c.game_loop()
