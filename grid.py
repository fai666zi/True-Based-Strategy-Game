# grid.py
import pygame
from constants import *

class Grid:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS

    def draw(self, win):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(win, GRAY, rect, 1)