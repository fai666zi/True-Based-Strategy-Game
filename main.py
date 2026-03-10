# main.py
import pygame
from constants import *
from game_engine import Game
import sys
import os
import random

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Strategy Game")
clock = pygame.time.Clock()

try:
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
except:
    print("Window icon not found, using default.")

start = False
font = pygame.font.SysFont("comicsansms",36)
player_icon_choice = "player1.png"
num_enemies = 1

icon_rects = [pygame.Rect(100,180,80,80), pygame.Rect(220,180,80,80)]
player_icons = ["player1.png", "player2.png"]
enemy_rects = [pygame.Rect(100 + i*80, 320, 60, 60) for i in range(2)]
start_rect = pygame.Rect(250,420,100,50)

while not start:
    win.fill(WHITE)
    win.blit(font.render("Mini Strategy Game", True, BLACK), (120,30))
    win.blit(pygame.font.SysFont("comicsansms",28).render("Rules: Move 2 cells, attack adjacent enemy", True, BLACK), (50,100))
    win.blit(font.render("Select Player Icon:", True, BLACK), (50,140))

    for idx, rect in enumerate(icon_rects):
        pygame.draw.rect(win, CYAN, rect)
        if player_icon_choice == player_icons[idx]:
            pygame.draw.rect(win,GREEN,rect,5)
        try:
            img = pygame.image.load(player_icons[idx])
            img = pygame.transform.scale(img,(rect.width-10,rect.height-10))
            win.blit(img,(rect.x+5,rect.y+5))
        except: pass

    win.blit(font.render("Select number of enemies:", True, BLACK), (50,280))
    for i, rect in enumerate(enemy_rects):
        pygame.draw.rect(win, ORANGE, rect)
        if num_enemies==i+1:
            pygame.draw.rect(win,GREEN,rect,5)
        win.blit(pygame.font.SysFont("comicsansms",28).render(str(i+1),True,BLACK),(rect.x+20,rect.y+20))

    pygame.draw.rect(win,GREEN,start_rect)
    win.blit(font.render("START",True,BLACK),(start_rect.x+15,start_rect.y+10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT: pygame.quit(); sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            for idx, rect in enumerate(icon_rects):
                if rect.collidepoint(x,y):
                    player_icon_choice = player_icons[idx]
            for i, rect in enumerate(enemy_rects):
                if rect.collidepoint(x,y):
                    num_enemies=i+1
            if start_rect.collidepoint(x,y):
                start=True

game = Game(player_icon_choice, num_enemies)
running = True

while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game.click(pos, win)

    game.enemy_turn(win)
    game.draw(win)
    pygame.display.update()

    winner = game.check_game_over()
    if winner:
        game_over = True
        while game_over:
            win.fill(WHITE)
            font2 = pygame.font.SysFont("comicsansms",48)
            win.blit(font2.render(winner, True, BLACK),(150,200))

            restart_rect = pygame.Rect(150,300,100,50)
            exit_rect = pygame.Rect(350,300,100,50)

            pygame.draw.rect(win,GREEN,restart_rect)
            pygame.draw.rect(win,RED,exit_rect)

            win.blit(font.render("RESTART", True, BLACK),(restart_rect.x+5,restart_rect.y+10))
            win.blit(font.render("EXIT", True, BLACK),(exit_rect.x+20,exit_rect.y+10))

            pygame.display.update()
            for e in pygame.event.get():
                if e.type==pygame.QUIT: pygame.quit(); exit()
                if e.type==pygame.MOUSEBUTTONDOWN:
                    x,y = e.pos
                    if restart_rect.collidepoint(x,y):
                        os.execv(sys.executable,['python']+sys.argv)
                    if exit_rect.collidepoint(x,y):
                        pygame.quit(); exit()

pygame.quit()   