from tkinter import *
import pygame
import levels
import constants
import os
import myIA
import random

class main():    

    def __init__(self):
        #### Village Var ####
        
        self.pop = 0
        self.popMax = 0
        self.BatimentPlacer = []
        self.Entity = []

        self.game = Tk()
        
        # Frame Ressource
        self.ressource = Frame(self.game, width=100, height=480)
        self.ressource.grid(row=0, column=0)
        self.ressourceLabel = Label(self.ressource, text="Ressource").pack()
        self.popLabel = Label(self.ressource, text=self.pop).pack()
        
        # Frame Select
        self.select = Frame(self.game, width=100, height=150)
        self.select.grid(row=1, column=0)
        
        # Frame Action
        self.action = Frame(self.game, width=500, height=150)
        self.action.grid(row=1, column=1)
        
        # Frame Game
        self.embed = Frame(self.game, width=640, height=480)
        self.embed.grid(row=0, column=1)
        
            # Init de pygame dans la frame Game
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        pygame.display.init()
        self.screen = pygame.display.set_mode(constants.TAILLE_FENETRE)
        
        self.current_level = levels.Level01(self.screen)
        
        self.done = False
        self.OnConstruct = False
        
        self.construct()
        self.clock = pygame.time.Clock()
        self.game.update()
        
        #### Main Loop ####
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selectionneur = levels.sprite(self)
                    pos = pygame.mouse.get_pos()
                    selectionneur.rect.x = pos[0]
                    selectionneur.rect.y = pos[1]
                    selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.movingSprite)
                    if selecting != None:
                        self.action.grid_forget()
                        self.select.grid_forget()
                        self.game.update()
                        x = selecting.sup
                        x.drawAction(self.game)
                    selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.villageoiSprite)
                    if selecting != None:
                        self.action.grid_forget()
                        self.select.grid_forget()
                        self.game.update()
                        x = selecting.sup
                        x.drawAction(self.game)
                        

            if self.OnConstruct:
                self.OnConstruct = self.build.onConstruct(event)
            self.current_level.update()
            self.current_level.drawing(self.screen)
            self.clock.tick(60)
            pygame.display.flip()
            self.game.update()
        pygame.quit()
    
    def construct(self):
        self.OnConstruct = True
        self.build = levels.comptoire("1.png", self.current_level)
    
    def IA(self, currentPos, goal):
        wall = []
        for x in range(int(constants.TAILLE_FENETRE[0]/10)):
            for y in range(int(constants.TAILLE_FENETRE[1]/10)):
                colisioneur = levels.sprite(self)
                colisioneur.rect.x = x * 10
                colisioneur.rect.y = y * 10
                colisioned = pygame.sprite.spritecollideany(colisioneur, self.current_level.staticSpriteColide)
                if colisioned != None:
                    wall.append((x,y))
        map = myIA.GridWithWeights(constants.TAILLE_FENETRE[0],constants.TAILLE_FENETRE[1])
        map.walls = wall
        cfrom, sfar = myIA.a_star_search(map, currentPos, goal)
        path = myIA.reconstruct_path(cfrom, currentPos, goal)
        print("chemin:",path)
        
    

if __name__ == "__main__":
    z = main()
    