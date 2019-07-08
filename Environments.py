class Environment:

    def __init__(self, scenario, max=100):


        self.action_space = (-1,0,1)
        self.max = max

        self.reset(scenario)

    def reset(self, scenario):
        self.steps = 0
        self.done = False

        self.current_state = scenario.board
        self.scenario = scenario

        return self.scenario.board

    def step(self, action):

        self.steps+=1

        self.scenario.step(action)
        self.done = self.steps > self.max or self.scenario.bang

        if self.scenario.bang:
            reward = -1
        else:
            reward =  0

        return self.scenario.board, reward, self.done, self.steps
