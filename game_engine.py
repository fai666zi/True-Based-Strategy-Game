# game_engine.py
import pygame
from constants import *
from grid import Grid
from unit import Unit
import random

class Game:
    def __init__(self, player_icon_path, num_enemies=1):
        self.grid = Grid()
        self.player = Unit(ROWS//2, 0, CYAN, player_icon_path)
        self.enemies = []

        num_enemies = min(num_enemies, 2)
        enemy_icons = ["enemy1.png", "enemy2.png"]
        for i in range(num_enemies):
            while True:
                row = random.randint(0, ROWS-1)
                col = COLS-1
                if all(e.row != row or e.col != col for e in self.enemies):
                    break
            self.enemies.append(Unit(row, col, ORANGE, enemy_icons[i]))

        self.units_turn_order = [self.player] + self.enemies
        self.current_turn_index = 0

    def draw(self, win):
        win.fill(WHITE)
        pygame.draw.rect(win, GRAY, (0,0,WIDTH,60))
        font = pygame.font.SysFont("comicsansms",24)
        win.blit(font.render(f"Player HP: {self.player.hp}", True, CYAN), (10,10))
        for idx,e in enumerate(self.enemies):
            win.blit(font.render(f"Enemy {idx+1} HP: {e.hp}", True, ORANGE), (WIDTH-160,10+idx*20))
        current_unit = self.units_turn_order[self.current_turn_index]
        unit_type = "Player" if current_unit==self.player else f"Enemy {self.enemies.index(current_unit)+1}"
        win.blit(font.render(f"Turn: {unit_type}", True, BLACK), (WIDTH//2-50,15))

        self.grid.draw(win)

        if current_unit==self.player:
            self.draw_movement_range(win)

        positions = {}
        for u in [self.player]+self.enemies:
            key = (u.row,u.col)
            if key not in positions: positions[key] = []
            positions[key].append(u)

        for key, units in positions.items():
            offsets = [(-10,0),(10,0),(0,10)]
            for idx, u in enumerate(units):
                off = offsets[idx] if idx<len(offsets) else (0,0)
                u.draw(win, offset=off)

    def draw_movement_range(self, win):
        for r in range(ROWS):
            for c in range(COLS):
                if self.player.distance(r,c) <= self.player.move_range:
                    rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(win, GREEN, rect, 3)

    def click(self, pos, win):
        current_unit = self.units_turn_order[self.current_turn_index]
        if current_unit!=self.player: return
        col = pos[0]//CELL_SIZE
        row = pos[1]//CELL_SIZE
        dist = self.player.distance(row,col)
        for enemy in self.enemies:
            if enemy.hp>0 and dist<=self.player.attack_range and row==enemy.row and col==enemy.col:
                self.animate_attack(win,self.player,enemy)
                enemy.hp -= 2
                self.next_turn()
                return
        occupied = any(e.row==row and e.col==col and e.hp>0 for e in self.enemies)
        if dist <= self.player.move_range and not occupied:
            self.player.move(row,col)
            self.next_turn()

    def enemy_turn(self, win):
        current_unit = self.units_turn_order[self.current_turn_index]
        if current_unit==self.player or current_unit.hp<=0: return

        if current_unit.distance(self.player.row,self.player.col)<=current_unit.attack_range:
            self.animate_attack(win,current_unit,self.player)
            self.player.hp -= 2
            self.next_turn()
            return

        possible_moves = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(possible_moves)
        for dr,dc in possible_moves:
            new_r = current_unit.row + dr
            new_c = current_unit.col + dc
            if 0<=new_r<ROWS and 0<=new_c<COLS:
                if not any(e.row==new_r and e.col==new_c and e!=current_unit for e in self.enemies):
                    if abs(new_r-self.player.row)+abs(new_c-self.player.col)<current_unit.distance(self.player.row,self.player.col):
                        current_unit.move(new_r,new_c)
                        break
        self.next_turn()

    def animate_attack(self, win, attacker, target):
        steps = 5
        for i in range(steps):
            x = attacker.col*CELL_SIZE + CELL_SIZE//2 + (target.col-attacker.col)*CELL_SIZE//2*(i+1)/steps
            y = attacker.row*CELL_SIZE + CELL_SIZE//2 + (target.row-attacker.row)*CELL_SIZE//2*(i+1)/steps
            self.draw(win)
            pygame.draw.circle(win, YELLOW, (int(x),int(y)), 8)
            pygame.display.update()
            pygame.time.delay(50)

    def next_turn(self):
        self.current_turn_index = (self.current_turn_index+1)%len(self.units_turn_order)
        while self.units_turn_order[self.current_turn_index].hp<=0:
            self.current_turn_index = (self.current_turn_index+1)%len(self.units_turn_order)

    def check_game_over(self):
        if self.player.hp<=0: return "Enemies win!"
        if all(e.hp<=0 for e in self.enemies): return "Player wins!"
        return None