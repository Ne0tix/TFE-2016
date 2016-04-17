# -*- coding: utf-8 -*-

import random
import time
import pygame
import sys
import pygame.constants as c
from pygame.locals import *

from ConstantesMap import *

class game(object):
    def __init__(self):
        pygame.key.set_repeat(50, 50)

    def GetEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                if event.key == K_b:
                    print("build")
                    z = Batiment(BUILD)
                    confirme = True
                    while confirme:
                        z.buildMove()
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_c:
                                    confirme = False
                    print("confirmed")


    def buildObject(self, objet, depX = 0, depY = 0):
        self.objet = objet
        for i, ligne in enumerate(self.objet):
            for j, case in enumerate(ligne):
                couleur = COLORS[case]
                self.position = j + depX, i + depY
                coord = tuple(self.position[k] * TAILLE_BLOCK[k] for k in range(2))
                pygame.draw.rect(surface, couleur, coord + TAILLE_BLOCK)
        print('object')
        self.rendre()

    def removeObject(self, objet, depX = 0, depY = 0):
        self.objet = objet
        for i, ligne in enumerate(self.objet):
            for j, case in enumerate(ligne):
                couleur = COLORS[MAP[i][j]]
                self.position = j + depX, i + depY
                coord = tuple(self.position[k] * TAILLE_BLOCK[k] for k in range(2))
                pygame.draw.rect(surface, couleur, coord + TAILLE_BLOCK)
            print('remove object')
            self.rendre()

    def rendre(self):
        print('rendre')
        pygame.display.update()
        clock.tick()

class Map(game):

    def __init__(self, carte):
        self.carte = carte
        game.__init__(self)
        self.buildObject(self.carte)

class Batiment():
    def __init__(self, bat):
        self.ball = pygame.image.load("1.png").convert_alpha()
        self.ballRect = self.ball.get_rect()
        surface.blit(self.ball, self.ballRect)
        pygame.display.flip()
        
    
    def buildMove(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    print('move RIGHT')
                    self.rect.rect.move(1*TAILLE_BLOCK[1],0)

                if event.key == K_LEFT:
                    print('move LEFT')
                    self.rect.rect.move(-1*TAILLE_BLOCK[1],0)

                if event.key == K_UP:
                    print('move UP')
                    self.rect.rect.move(0, -1*TAILLE_BLOCK[1])

                if event.key == K_DOWN:
                    print('move DOWN')
                    self.rect.rect.move(0, 1*TAILLE_BLOCK[1])



if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode(TAILLE_FENETRE)
    pygame.display.set_caption('My app')
    J = Map(MAP)
    G = game()
    
    while True:
        G.GetEvent()
