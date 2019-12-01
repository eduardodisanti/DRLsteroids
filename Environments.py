
class Environment:

    def __init__(self, scenario, max=100):


        self.action_space = (-1,0,1)
        self.max = max

        self.scenario = scenario
        self.reset()

    def reset(self):
        self.steps = 0
        self.done = False

        self.scenario.reset()
        self.current_state = self.scenario.board
        self.scenario = self.scenario

        return self.scenario.board

    def compute_min_distance(self, board, ship):

        shape, x, y = ship

        lastline = board[y]

        mindist = len(lastline)
        for i in range(0, len(lastline)):
            if lastline[i] == 1:
                dist = min(abs(i - x), mindist)

                if dist < mindist:
                    mindist = dist

        return mindist / 100

    def step(self, action):

        self.steps+=1

        self.scenario.step(action)
        self.done = self.steps > self.max or self.scenario.bang

        mult = 0
        if self.steps % self.scenario.height==0:
            mult = self.compute_min_distance(self.scenario.board, self.scenario.get_ship())

        if self.scenario.bang:
            reward = -100
        else:
            reward =  mult


        return self.scenario.board, reward, self.done, self.steps
