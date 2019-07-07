class Environment:

    def __init__(self, scenario, max=100):


        self.action_space = (-1,1)
        self.steps = 0
        self.done = False
        self.max = max

        self.current_state = scenario.board
        self.scenario = scenario


    def step(self, action):

        self.steps+=1

        self.done = self.steps > self.max or self.scenario.bang

        reward = self.scenario.score

        return reward

