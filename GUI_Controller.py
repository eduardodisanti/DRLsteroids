from tkinter import *

import time

from Scenarios import Scenario


class Controller:

    def __init__(self, scenario, canvas, graphic_size=(200,200)):

        w, h = graphic_size
        self.scenario = scenario
        self.graphic_w = w
        self.graphic_h = h
        self.speed = 0.01
        self.scene = Scenario(size=(40, 20), density=10)

        self.canvas = canvas
        #self.ship = Ship()

    def draw_scenario(self):

        h = self.scenario.height
        w = self.scenario.width

        for i in range(0, h):
            for j in range(0, w):
                x1 = j * 10
                x2 = x1 + 10
                y1 = i * 10
                y2 = y1 + 10
                self.canvas.create_oval(x1, y1, x2, y2)


    def game_loop(self):
        master = Tk()
        canvas_height = self.scenario.height
        canvas_width = self.scenario.height

        while True:
            self.draw_scenario()
            mainloop()

            time.sleep(self.speed)
            print(".", end="")


tk = Tk()
tk.title = "Survive"
tk.resizable(100, 100)
canvas = Canvas(tk, width=200, height=200, bd=0, highlightthickness=0)
s = Scenario(size=(20, 20), density=10)
c = Controller(s, canvas, graphic_size=(200,200))
c.game_loop()