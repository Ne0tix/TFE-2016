# -*- coding: utf-8 -*-

import random
import time
import pygame
import sys
from pygame.locals import *

from ConstantesMap import *

class game(object):

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
                    while pygame.event.get() != K_0:
                        z.buildMove()
                    print("confimed")

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

    def rendre(self):
        print('rendre')
        pygame.display.update()
        clock.tick()

class Map(game):

    def __init__(self, carte):
        self.carte = carte
        game.__init__(self)
        self.buildObject(self.carte)

class Batiment(game):

    def __init__(self, bat):
        self.build = bat
        game.__init__(self)
        self.buildObject(self.build)
        self.posX = 0
        self.posY = 0
    
    def buildMove(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    print('move RIGHT')
                    self.posX += 1
                    self.buildObject(self.build, self.posX, self.posY)
                if event.key == K_LEFT:
                    print('move LEFT')
                    self.posX -= 1
                    self.buildObject(self.build, self.posX, self.posY)
                if event.key == K_UP:
                    print('move UP')
                    self.posY -= 1
                    self.buildObject(self.build, self.posX, self.posY)
                if event.key == K_DOWN:
                    print('move DOWN')
                    self.posY += 1
                    self.buildObject(self.build, self.posX, self.posY)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode(TAILLE_FENETRE)
    pygame.display.set_caption('My app')
    J = Map(MAP)
    G = game()
    
    while True:
        G.GetEvent()
