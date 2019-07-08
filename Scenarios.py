import random
import time


THE_MARK = "*"
BLANK    = " "
class Scenario:

    def __init__(self, ship, size=(64,64), density=10):

        w, h = size
        self.top = 0
        self.height = h
        self.width = w
        self.density = density

        self.board = [[0]*(w) for i in range(h)]

        self.ship = ship

        self.ship_shape, _, _ = ship
        self.bang = False
        self.score = 0

    def step(self, action):

        s, x, y = self.ship
        x+=action
        self.ship = (s,x,y)
        self.put_ship(self.ship)
        self.move_down_scenario(1)

    def print_scenario(self):
        for j in range(self.height):
            for i in range(self.width):

                    if self.board[j][i] == 1:
                        mark = THE_MARK
                    elif self.board[j][i]  == -1:
                        mark = self.ship_shape
                    else:
                        mark =  BLANK
                    print(mark, end="")
            print("")

    def create_new_line(self, i):
        self.board[i] = [0]*self.width
        for j in range(self.width):
            if random.randint(0, 100) <= self.density:
                self.board[i][j] = 1

    def create_world(self):
        for i in range(self.height):
            self.create_new_line(i)

    def move_up_scenario(self, num_lines):
        for index in range(1, self.height - 1):
            self.board[index] = self.board[index + 1]
        self.create_new_line(index + 1)

    def move_down_scenario(self, num_lines):
        for index in range(self.height - 1, 1, -1):
            self.board[index] = self.board[index - 1]
        self.create_new_line(index - 1)

        pts = sum(self.board[self.height - 1])
        self.score += pts

    def get_object_on(self, x, y):

        return self.board[y][x]

    def put_ship(self, ship):

        self.ship = ship
        y = int(self.ship[2] - 1)
        x = int(self.ship[1] - 1)

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x >= self.width - 1:
            x = self.width - 1


        next_1 = self.board[y][x]
        self.board[y][x] = -1

        next = self.board[y - 1][x]

        self.bang = next != 0 or next_1 != 0

        if self.bang:
            self.score += 10

        return self.bang

#s = Scenario(size=(40, 20), density=10)

#s.print_scenario()
#for _ in range(0,1000):
#    print("\033[H\033[J")
#    s.move_down_scenario(1)
#    s.print_scenario()
#    time.sleep(0.1)