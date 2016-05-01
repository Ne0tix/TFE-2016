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
                self.position = j + depX, i + depY
                coord = tuple(self.position[k] * TAILLE_BLOCK[k] for k in range(2))
                img = IMG[case]
                imgRect = img.get_rect()
                imgRect.move_ip(coord)
                surface.blit(img, imgRect)
        print('object')
        self.rendre()

    def removeObject(self, depX = 0, depY = 0, tailleX=0, tailleY=0):
        for i in range(tailleY):
            for j in range(tailleX):
                #couleur = IMG[case]
                self.position = j + depX, i + depY
                coord = tuple(self.position[k] * TAILLE_BLOCK[k] for k in range(2))
                img = IMG[2]
                imgRect = img.get_rect()
                imgRect.move_ip(coord)
                surface.blit(img, imgRect)
        print('remove object')
        self.rendre()

    def rendre(self):
        print('rendre')
        pygame.display.flip()
        pygame.display.update()
        clock.tick()

class Map(game):


    def __init__(self):
        game.__init__(self)
        print(int(TAILLE_FENETRE[0]/TAILLE_BLOCK[0]), int(TAILLE_FENETRE[1]/TAILLE_BLOCK[1]))
        self.carte = self.GenerateMap(int(TAILLE_FENETRE[0]/TAILLE_BLOCK[0]), int(TAILLE_FENETRE[1]/TAILLE_BLOCK[1]))
        self.buildObject(self.carte)

    def first(self, y):
        det = random.randint(1, 100)                
        if det >= 95:
            self.map[y].append(4)
        if det >= 50 and det < 95:
            self.map[y].append(1)
        if det >= 5 and det < 50:
            self.map[y].append(2)
        if det < 5:
            self.map[y].append(3)

    def generateBy1(self,y):
        det = random.randint(1,100)
        if det >= 95:
            self.map[y].append(4)
        if det >= 40 and det < 95:
            self.map[y].append(1)
        if det >= 5 and det < 40:
            self.map[y].append(2)
        if det < 5:
            self.map[y].append(3)

    def generateBy2(self, y):
        det = random.randint(1,100)
        if det >= 95:
            self.map[y].append(4)
        if det >= 55 and det < 95:
            self.map[y].append(1)
        if det >= 5 and det < 55:
            self.map[y].append(2)
        if det < 5:
            self.map[y].append(3)

    def generateBy3(self, y):
        det = random.randint(1,100)
        if det >= 5:
            self.map[y].append(4)
        if det >= 70 and det < 5:
            self.map[y].append(1)
        if det >= 10 and det < 70:
            self.map[y].append(2)
        if det < 10:
            self.map[y].append(3)

    def generateBy4(self, y):
        det = random.randint(1,100)
        if det >= 90:
            self.map[y].append(4)
        if det >= 40 and det < 90:
            self.map[y].append(1)
        if det >= 3 and det < 40:
            self.map[y].append(2)
        if det < 3:
            self.map[y].append(3)


    def GenerateMap(self, MaxX, MaxY):
        self.map = []
        for y in range(MaxY):
            self.map.append([])
            for x in range(MaxX):
                if self.map == [[]]:
                    print("first")
                    print(y)
                    self.first(y)
                else:
                    if y == 0:
                        ## first line ##
                        if self.map[y][x-1] == 1:
                            self.generateBy1(y)
                        elif self.map[y][x-1] == 2:
                            self.generateBy2(y)
                        elif self.map[y][x-1] == 3:
                            self.generateBy3(y)
                        elif self.map[y][x-1] == 4:
                            self.generateBy4(y)
                    elif x-1 < 0:
                        if self.map[y-1][x] == 1:
                            self.generateBy1(y)
                        elif self.map[y-1][x] == 2:
                            self.generateBy2(y)
                        elif self.map[y-1][x] == 3:
                            self.generateBy3(y)
                        elif self.map[y-1][x] == 4:
                            self.generateBy4(y)
                    else:
                        if self.map[y][x-1] == 1:
                            self.generateBy1(y)
                        elif self.map[y][x-1] == 2:
                            self.generateBy2(y)
                        elif self.map[y][x-1] == 3:
                            self.generateBy3(y)
                        elif self.map[y][x-1] == 4:
                            self.generateBy4(y)
        return self.map

class Batiment(game):
    def __init__(self, bat):
        game.__init__(self)
        self.ball = pygame.image.load("1.png").convert_alpha()
        self.ballRect = self.ball.get_rect()
        self.posX = 0
        self.posY = 0
        surface.blit(self.ball, self.ballRect)
        pygame.display.update()
        
    
    def buildMove(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    print('move RIGHT')
                    self.removeObject(self.posX, self.posY, 3, 3)              
                    self.ballRect.move_ip(1*TAILLE_BLOCK[1],0)
                    self.posX += 1
                    surface.blit(self.ball, self.ballRect)
                    pygame.display.update()

                if event.key == K_LEFT:
                    print('move LEFT')
                    self.removeObject(self.posX, self.posY, 3, 3)              
                    self.ballRect.move_ip(-1*TAILLE_BLOCK[1],0)
                    self.posX -= 1
                    surface.blit(self.ball, self.ballRect)
                    pygame.display.update()

                if event.key == K_UP:
                    print('move UP')
                    self.removeObject(self.posX, self.posY, 3, 3)              
                    self.ballRect.move_ip(0,-1*TAILLE_BLOCK[1])
                    self.posY -= 1
                    surface.blit(self.ball, self.ballRect)
                    pygame.display.update()
                if event.key == K_DOWN:
                    print('move DOWN')
                    self.removeObject(self.posX, self.posY, 3, 3)              
                    self.ballRect.move_ip(0,1*TAILLE_BLOCK[1])
                    self.posY += 1
                    surface.blit(self.ball, self.ballRect)
                    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode(TAILLE_FENETRE)
    pygame.display.set_caption('My app')
    J = Map()
    G = game()
    
    while True:
        G.GetEvent()
