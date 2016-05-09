import pygame
import constants
import sprite
from tkinter import *

class Level(object):
    staticSpriteColide = None
    movingSprite = None
    villageoiSprite = None
    
    #self.batimentPlacer = []
    #self.entity = []    
    background = None
    
    def __init__(self):
        self.staticSpriteColide = pygame.sprite.Group()
        self.movingSprite = pygame.sprite.Group()
        self.villageoiSprite = pygame.sprite.Group()
        
    def update(self):
        self.staticSpriteColide.update()
        self.movingSprite.update()
    
    def drawing(self, screen):
        screen.fill((0, 255, 0))
        screen.blit(self.background, (0,0))

        self.staticSpriteColide.draw(screen)
        self.movingSprite.draw(screen)

class Level01(Level):
    def __init__(self, screen):
        Level.__init__(self)
        self.screen = screen
        
        self.background = pygame.image.load("Background.png").convert()
        self.background.set_colorkey((0, 255, 0))
        
        levelInit = [ 
                ['Wall640.png', 0, 0],
                ["Wall640.png", 0, 47],
                ["wall480.png", 0, 0],
                ["wall480.png", 63, 0],
                ["Lac.png", 32, 24],
                ]
        for objet in levelInit:
            block = sprite(self, objet[0])
            block.rect.x = objet[1]*10
            block.rect.y = objet[2]*10
            self.staticSpriteColide.add(block)
        '''
        batimentInit = [
                ["1.png", 25, 15],
                ]
        for objet in batimentInit:
            block = sprite(objet[0])
            block.rect.x = objet[1]*10
            block.rect.y = objet[2]*10
            self.staticSpriteColide.add(block)
            self.batimentPlacer.append(block)
        entityInit = [
                ["char.png", 25, 19],
                ["char.png", 26, 19],
                ["char.png", 28, 19]
        ]
        for objet in entityInit:
            block = sprite(objet[0])
            block.rect.x = objet[1]*10
            block.rect.y = objet[2]*10
            self.movingSprite.add(block)
          '''  
class batiment():
    '''
    action = Frame(TFE.main.main.game, width=500, height=150)
    action.grid(row=1, column=1)
    VillageoiButton = Button(action, text="Villgeoi", command=test)
    '''
    def __init__(self, image, level):
        self.building = sprite(self,image)
        self.buildPos = (10, 10)
        self.cLevel = level
        self.cLevel.movingSprite.add(self.building)
    
        
    def moveBatiment(self, x, y):
        mod10X = x%10
        mod10Y = y%10
        self.building.rect.x = int(x-mod10X)
        self.building.rect.y = int(y-mod10Y)
        self.buildPos = (x, y)
        
    def place(self):
        self.cLevel.movingSprite.remove(self.building)
        self.cLevel.movingSprite.add(self.building)
        
    def onConstruct(self, event):
        pos = pygame.mouse.get_pos()
        self.moveBatiment(pos[0],pos[1])
        OnConstruct = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            OnConstruct = False
            self.place()
        return OnConstruct
    

class comptoire(batiment):
    def __init__(self, image, level):
        batiment.__init__(self, image, level)
        self.vie = 30
        self.vieMax = 30
    
    def drawAction(self, fen):
        action = Frame(fen, width=500, height=150)
        action.grid(row=1, column=1)
        VillageoiButton = Button(action, text="villageoi", command= lambda: self.vill())
        VillageoiButton.grid(row=1, column=1)
    
    def vill(self):
        x = villageoi(self.cLevel)


class pierre(batiment):
    def __init__(self, image, level):
        batiment.__init__(self, image, level)
        self.vie = 30
        self.vieMax = 30

    def drawAction(self, fen):
        action = Frame(fen, width=500, height=150)
        action.grid(row=1, column=1)
        VillageoiButton = Button(action, text="Pierre")
        VillageoiButton.grid(row=1, column=1)

class foret(batiment):
    def __init__(self, image, level):
        batiment.__init__(self, image, level)
        self.vie = 30
        self.vieMax = 30

    def drawAction(self, fen):
        action = Frame(fen, width=500, height=150)
        action.grid(row=1, column=1)
        VillageoiButton = Label(action, text="Foret")
        VillageoiButton.grid(row=1, column=1)
        
class sprite(pygame.sprite.Sprite):

    def __init__(self, sup, imageData=None):
        self.sup = sup
        pygame.sprite.Sprite.__init__(self)
        if imageData != None:
            self.image = pygame.image.load(imageData).convert_alpha()
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((10,10))
            self.rect = self.image.get_rect()
        
        
class villageoi():
    def __init__(self, level):
        self.villageoiSprite = sprite(self,"char.png")
        self.vie = 30
        self.vieMax = 30
        self.villageoiSprite.rect.x = 10
        self.villageoiSprite.rect.y = 10
        self.cLevel = level
        self.cLevel.movingSprite.add(self.villageoiSprite)
        
    def drawAction(self, fen):
        # Frame Action
        action = Frame(fen, width=500, height=150)
        action.grid(row=1, column=1)
        
        pierreButton = Button(action, text="pierre", command= lambda:self.pierre())
        pierreButton.grid(row=1, column=1)
        
        foretButton = Button(action, text="foret", command= lambda:self.foret())
        foretButton.grid(row=1, column=2)
        
        # Frame Select
        select = Frame(fen, width=100, height=150)
        select.grid(row=1, column=0)
        
        VieLabel = Label(select, text=self.vie)
        VieMaxLabel = Label(select, text=self.vieMax)
        VieLabel.grid(row=0, column=0)
        VieMaxLabel.grid(row=0, column=1)
        
    def pierre(self):
        bat = pierre("pierreRessource.png", self.cLevel)
        onConstruct = True
        while onConstruct:
            for event in pygame.event.get():
                onConstruct = bat.onConstruct(event)
                
        
        
    def foret(self):
        bat = foret("ForetRessource.png", self.cLevel)
        onConstruct = True
        while onConstruct:
            for event in pygame.event.get():
                onConstruct = bat.onConstruct(event)
        
        

        