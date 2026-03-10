# unit.py
import pygame
from constants import *

class Unit:
    def __init__(self, row, col, color, icon=None):
        self.row = row
        self.col = col
        self.color = color
        self.hp = 10
        self.move_range = 2
        self.attack_range = 1
        self.icon = icon

    def draw(self, win, offset=(0,0)):
        x = self.col*CELL_SIZE + CELL_SIZE//2 + offset[0]
        y = self.row*CELL_SIZE + CELL_SIZE//2 + offset[1]
        if self.icon:
            try:
                img = pygame.image.load(self.icon)
                img = pygame.transform.scale(img, (CELL_SIZE-10, CELL_SIZE-10))
                win.blit(img, (x - img.get_width()//2, y - img.get_height()//2))
            except:
                pygame.draw.circle(win, self.color, (x,y), CELL_SIZE//3)
        else:
            pygame.draw.circle(win, self.color, (x,y), CELL_SIZE//3)

    def move(self, row, col):
        self.row = row
        self.col = col

    def distance(self, row, col):
        return abs(self.row-row) + abs(self.col-col)