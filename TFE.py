from tkinter import *
from pygame.locals import *
import pygame
import constants
import os
import myIA
import random

class main():    

    def __init__(self):
        #### Village Var ####
        
        self.game = Tk()
        self.game.resizable(width=False, height=False)
        
        # Frame Ressource
        self.ressource = LabelFrame(self.game, text="Ressource", width=500, height=150)
        self.ressource.grid(row=1, column=1)
                      
        # Frame Select
        self.select = LabelFrame(self.game, text="Select", width=100, height=150)
        self.select.grid(row=1, column=0)
        
        # Frame Action
        self.action = LabelFrame(self.game, text="Action", width=100, height=480)
        self.action.grid(row=0, column=0)
        
        # Frame Game
        self.embed = Frame(self.game, width=640, height=480)
        self.embed.grid(row=0, column=1)
        
            # Init de pygame dans la frame Game
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        pygame.display.init()
        self.screen = pygame.display.set_mode(constants.TAILLE_FENETRE)
        
        self.current_level = Level01(self.screen)
                
        self.clock = pygame.time.Clock()
        self.second = 0
        pygame.time.set_timer(USEREVENT + 1, 300) # Timer déplacement
        pygame.time.set_timer(USEREVENT + 2, 500) # Timer Action
        self.actionToDo = {}
        self.currentSelected = None

                
        #### Main Loop ####
        while True:

            for item in self.ressource.winfo_children(): # Destruction de l intérieur de la frame ressource
                item.destroy()
                
            ### Partie Gestion de la Frame Ressource ###
            keys = []
            values = []
                ### Recuperation des informations et valeurs des ressource utlisé
            for key in self.current_level.ressource.keys():         
                keys.append(key)                                    
                                                                    
            for value in self.current_level.ressource.values():        
                values.append(value)                                
                
                ### Affichage des ressource
            for position in range(len(keys)):
                labelname = Label(self.ressource, text=keys[position])
                labelname.grid(row=0, column=position)
                
                labelitem = Label(self.ressource, text=values[position])
                labelitem.grid(row=1, column=position)
                
            ### Gestion des évènement ###
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT: # On quit game
                    pygame.quit()
                    sys.quit()
                
                ### Action de deplacement
                if self.currentSelected != None:
                    if self.currentSelected.moveActive:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.currentSelected != None:
                                pos = pygame.mouse.get_pos()
                                self.chemin = self.IA(((self.currentSelected.positionX), (self.currentSelected.positionY)), (int((pos[0])/10),int((pos[1])/10)) )
                                self.actionToDo[self.currentSelected] = self.chemin
                                self.currentSelected.moveActive = False
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event)
                ### Outil de selection ###
                    selectionneur = sprite()
                    pos = pygame.mouse.get_pos()
                    selectionneur.moveSprite(pos)
                    
                    ### Colision with any build
                    selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.staticSprite)                    
                    if selecting != None:
                        for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                            item.destroy()
                            
                        for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                            item.destroy()
                        
                        selecting.drawAction(self) # Dessin de la nouvelle frame
                        self.currentSelected = None
                        
                    ### Colision with any Entity
                    selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.entitySprite)
                    if selecting != None:
                        for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                            item.destroy()
                            
                        for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                            item.destroy()
                        
                        selecting.drawAction(self) # Dessin de la nouvelle Frame
                        self.currentSelected = selecting
                    
                    ### Colision with any ressource
                    selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.ressourceSprite)
                    if selecting != None:
                        for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                            item.destroy()
                            
                        for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                            item.destroy()
                        
                        selecting.drawAction(self) # Dessin de la nouvelle Frame
                        self.currentSelected = None
                                                
                   
                if event.type == USEREVENT +1: # Toute les 300ms
                    for action in self.actionToDo:
                        self.actionList = self.actionToDo[action]
                        if len(self.actionList) != 0:
                            self.indice = self.actionList.pop(0)
                            action.move(self.indice)
                            
                    self.second += 1
                
                if event.type == USEREVENT + 2: # Toute les 500ms
                    for entity in self.current_level.entitySprite:
                        producer = pygame.sprite.spritecollideany(entity, self.current_level.ressourceSprite)
                        if producer != None:
                            self.current_level.ressource[producer.product] += 1
                            if producer.currentRessource != 0:
                                producer.currentRessource -= 1
                                if self.currentSelected == None:
                                    for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                                        item.destroy()
                                        
                                    for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                                        item.destroy()
                                    producer.drawAction(self.game)
                            else:
                                self.current_level.ressourceSprite.remove(producer)
                            
  
                            
                        
                        
                for objet in self.current_level.movingSprite:
                    pos = pygame.mouse.get_pos()
                    objet.move((int(pos[0]/10), int(pos[1])/10))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.current_level.movingSprite.remove(objet)
                        self.current_level.staticSprite.add(objet)
                                        
            ### Draw level and update ###
            self.current_level.update()
            self.current_level.drawing(self.screen)
            self.clock.tick(60)
            pygame.display.flip()
            self.game.update()
                    
    def IA(self, currentPos, goal):
        wall = []
        for x in range(int(constants.TAILLE_FENETRE[0]/10)):
            for y in range(int(constants.TAILLE_FENETRE[1]/10)):
                colisioneur = sprite()
                colisioneur.rect.x = x * 10
                colisioneur.rect.y = y * 10
                colisioned = pygame.sprite.spritecollideany(colisioneur, self.current_level.wallSpriteColide)
                if colisioned != None:
                    wall.append((x,y))
        map = myIA.GridWithWeights(constants.TAILLE_FENETRE[0],constants.TAILLE_FENETRE[1])
        map.walls = wall
        cfrom, sfar = myIA.a_star_search(map, currentPos, goal)
        path = myIA.reconstruct_path(cfrom, currentPos, goal)
        return path
        
class Level(object):
    def __init__(self):
        self.wallSpriteColide = pygame.sprite.Group()
        self.movingSprite = pygame.sprite.Group()
        self.staticSprite = pygame.sprite.Group()
        self.entitySprite = pygame.sprite.Group()
        self.ressourceSprite = pygame.sprite.Group()
        self.ressource = {}
        
    def update(self):
        self.wallSpriteColide.update()
        self.movingSprite.update()
        self.staticSprite.update()
        self.entitySprite.update()
        self.ressourceSprite.update()
        
    
    def drawing(self, screen):
        screen.fill((0, 255, 0))
        screen.blit(self.background, (0,0))

        self.wallSpriteColide.draw(screen)
        self.movingSprite.draw(screen)
        self.staticSprite.draw(screen)
        self.ressourceSprite.draw(screen)
        self.entitySprite.draw(screen)

class Level01(Level):
    def __init__(self, screen):
        Level.__init__(self)
        self.screen = screen
        
        self.background = pygame.image.load(constants.imgBackground).convert()
        self.background.set_colorkey((0, 255, 0))
        
        levelInit = [ 
                [constants.imgWall640, 0, 0],
                [constants.imgWall640, 0, 47],
                [constants.imgWall480, 0, 0],
                [constants.imgWall480, 63, 0],
                [constants.imgLac, 32, 24],
                ]
                
        for objet in levelInit:
            block = sprite(objet[0])
            block.rect.x = objet[1]*10
            block.rect.y = objet[2]*10
            self.wallSpriteColide.add(block)
        
        levelRessource = [
            [bois, (12, 12)],
            [bois, (13, 14)],
            [bois, (16, 15)],
            [bois, (25, 19)],
            [pierre, (20, 30)],
            [pierre, (23, 28)],
            [pierre, (17, 33)],
            [nourriture, (30, 45)],
            [nourriture, (33, 42)]
        ]
        
        for ressource in levelRessource:
            x = ressource[0](self, ressource[1])
            self.ressourceSprite.add(x)
            
        self.first = comptoire(self.screen, (2,2)) # Creation du 1ere batiment
        self.staticSprite.add(self.first)
        
        self.villager1 = villageoi(self, (5,5))
        self.entitySprite.add(self.villager1)
        
        self.villager2 = villageoi(self, (6, 6))
        self.entitySprite.add(self.villager2)

            
class entity(pygame.sprite.Sprite):
    def __init__(self, level, position):
        pygame.sprite.Sprite.__init__(self)
        self.currentLevel = level
        self.positionX = position[0]
        self.positionY = position[1]
    
    def loadImg(self, img, position):
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]*10    
        self.rect.y = position[1]*10     
            
    def move(self, pos):
        self.positionX = (pos[0])
        self.positionY = (pos[1])
        self.rect.x = self.positionX*10
        self.rect.y = self.positionY*10

class comptoire(entity):
    def __init__(self, level, position):
        entity.__init__(self, level, position)
        self.vie = 30
        self.vieMax = 30
        self.invent = 0
        self.inventMax = 30
        self.loadImg(constants.imgComptoire, position)
        
    def drawAction(self, fen):
        Label.test = Label(fen.action, text="Test")
        Label.test.grid()

class woodFarm(entity):
    def __init__(self, level, position):
        entity.__init__(self, level, position)
        self.vie = 30
        self.vieMax = 30
        self.loadImg(constants.imgWoodFarm, position)

class ressource(entity):
    def __init__(self, level, position):
        entity.__init__(self, level, position)
        self.currentRessource = 300
        self.ressource = 300
        
class pierre(ressource):
    def __init__(self, level, position):
        ressource.__init__(self, level, position)
        self.loadImg(constants.imgPierre, position)
        self.product = "Pierre"
        level.ressource[self.product] = 0
        

    def drawAction(self, fen):                
        self.nameRessouceLabel = Label(fen.select, text="Pierre")
        self.nameRessouceLabel.grid(row=0, column=0)
        
        self.ressourceLabel = Label(fen.select, text="Ressource :")
        self.ressourceLabel.grid(row=1, column=0)
        
        self.currentRessourceLabel = Label(fen.select, text=self.currentRessource)
        self.currentRessourceLabel.grid(row=1, column=1)

class bois(ressource):
    def __init__(self, level, position):
        ressource.__init__(self, level, position)
        self.loadImg(constants.imgArbre, position)
        self.product = "Bois"
        level.ressource[self.product] = 0
        

    def drawAction(self, fen):        
        self.nameRessouceLabel = Label(fen.select, text="Bois")
        self.nameRessouceLabel.grid(row=0, column=0)
        
        self.ressourceLabel = Label(fen.select, text="Ressource :")
        self.ressourceLabel.grid(row=1, column=0)
        
        self.currentRessourceLabel = Label(fen.select, text=self.currentRessource)
        self.currentRessourceLabel.grid(row=1, column=1)

class nourriture(ressource):
    def __init__(self, level, position):
        ressource.__init__(self, level, position)
        self.loadImg(constants.imgnourriture, position)
        self.product = "nourriture"
        level.ressource[self.product] = 0
        

    def drawAction(self, fen):        
        self.nameRessouceLabel = Label(fen.select, text="nourriture")
        self.nameRessouceLabel.grid(row=0, column=0)
        
        self.ressourceLabel = Label(fen.select, text="Ressource :")
        self.ressourceLabel.grid(row=1, column=0)
        
        self.currentRessourceLabel = Label(fen.select, text=self.currentRessource)
        self.currentRessourceLabel.grid(row=1, column=1)

        
        
        
class sprite(pygame.sprite.Sprite):

    def __init__(self, imageData=None):
        pygame.sprite.Sprite.__init__(self)
        
        if imageData != None:
            self.image = pygame.image.load(imageData).convert_alpha()
            self.rect = self.image.get_rect()
            
        else:
            self.image = pygame.Surface((10,10))
            self.rect = self.image.get_rect()
        
    def moveSprite(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]
                
class villageoi(entity):
    def __init__(self, level, position):
        entity.__init__(self, level, position)
        self.vie = 30
        self.vieMax = 30
        self.loadImg(constants.imgChar, position)
        self.moveActive = False
        
    def drawAction(self, fen):
        # Frame Action
        moveButton = Button(fen.action, text="Move", command= lambda: self.moveEntity())
        moveButton.grid(row=1, column=3)
        
        woodFarmButton = Button(fen.action, text="Wood Farm", command= lambda: self.buildWoodFarm())
        woodFarmButton.grid(row=1, column=4)
        
        # Frame Select        
        VieLabel = Label(fen.select, text=self.vie)
        VieMaxLabel = Label(fen.select, text=self.vieMax)
        VieLabel.grid(row=0, column=0)
        VieMaxLabel.grid(row=0, column=1)
        
    def moveEntity(self):
        self.moveActive = True
    
    def buildWoodFarm(self):
        x = woodFarm(self.currentLevel, (10,10))
        if self.currentLevel.ressource["Bois"] - 100 < 0 or self.currentLevel.ressource["Pierre"] -100 < 0:
            print("Construction imposible")
        else:
            self.currentLevel.movingSprite.add(x)
            
if __name__ == "__main__":
    z = main()
    