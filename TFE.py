from tkinter import *
from pygame.locals import *
import pygame
import constants
import os
import myIA
import random
import datetime
import sqlite3
import mainMenu


class main():    

    def __init__(self, user, load=False, save=None):
        
        self.user = user
        self.saveName = save
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
        
        # Autre
        self.saveButton = Button(self.game, text="Save", command= lambda: self.mSave())
        self.saveButton.grid()
        
        self.backToMainmenu = Button(self.game, text="Back to menu", command= lambda: self.backToMainMenu())
        self.backToMainmenu.grid()
        
        # Frame Game
        self.embed = Frame(self.game, width=640, height=480)
        self.embed.grid(row=0, column=1)
        
            # Init de pygame dans la frame Game
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        pygame.display.init()
        self.screen = pygame.display.set_mode(constants.TAILLE_FENETRE)
        
        if load:
            conn = sqlite3.connect("DataBase/"+self.saveName[0]+".db3")
            c = conn.cursor()
            
            c.execute("SELECT CurrentLevel from Level")
            for row in c:
                self.current_level = eval(row[0]+"(self.screen)")
                for objet in self.current_level.ressourceSprite:
                    self.current_level.ressourceSprite.remove(objet)
                
                for objet in self.current_level.staticSprite:
                    self.current_level.staticSprite.remove(objet)
                
                for objet in self.current_level.entitySprite:
                    self.current_level.entitySprite.remove(objet)
            
            c.execute("SELECT ClassName, Position from RessourceSprite")
            for row in  c:
                x = ressource(self.current_level, eval(row[1]), row[0])
                self.current_level.ressourceSprite.add(x)
            
            c.execute("SELECT className, Position from StaticSprite")
            for row in c:
                x = build(self.current_level, eval(row[1]), row[0])
                self.current_level.staticSprite.add(x)
            
            c.execute("SELECT className, position from entitySprite")
            for row in c:
                x = villageoi(self.current_level, eval(row[1]))
                self.current_level.entitySprite.add(x)
            
            conn.commit()
            c.close()
        else:
            self.current_level = Level01(self.screen)
                
        self.clock = pygame.time.Clock()
        self.second = 0
        pygame.time.set_timer(USEREVENT + 1, 300) # Timer déplacement
        pygame.time.set_timer(USEREVENT + 2, 500) # Timer Action
        pygame.time.set_timer(USEREVENT + 3, 1500)
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
                    self.game.quit()
                    sys.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[2]: # Clic droit
                        if self.currentSelected != None:
                            if str(self.currentSelected[1]) == "villageoi":
                                selectionneur = sprite()
                                pos = pygame.mouse.get_pos()
                                selectionneur.moveSprite(pos)

                                wrongWall = pygame.sprite.spritecollideany(selectionneur, self.current_level.wallSpriteColide)
                                wrongBuild = pygame.sprite.spritecollideany(selectionneur, self.current_level.staticSprite)
                                wrongEntity = pygame.sprite.spritecollideany(selectionneur, self.current_level.entitySprite)
                                wrongRessource = pygame.sprite.spritecollideany(selectionneur, self.current_level.ressourceSprite)
                                if wrongWall != None or wrongBuild != None or wrongEntity != None or wrongRessource != None:
                                    pass
                                else:
                                    self.chemin = self.IA(((self.currentSelected[0].positionX), (self.currentSelected[0].positionY)), (int(((pos[0])/10)),int(((pos[1])/10))))
                                    self.actionToDo[self.currentSelected[0]] = self.chemin

                    if pygame.mouse.get_pressed()[0]: # Clic gauche
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
                            self.currentSelected = (selecting, selecting.__class__.__name__) # Recupere le nom de la classe instantié
                                                                            
                        ### Colision with any ressource
                        selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.ressourceSprite)
                        if selecting != None:
                            for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                                item.destroy()
                                
                            for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                                item.destroy()
                            
                            selecting.drawAction(self) # Dessin de la nouvelle Frame
                            self.currentSelected = (selecting, selecting.__class__.__name__)
                            
                        ### Colision with any Entity
                        selecting = pygame.sprite.spritecollideany(selectionneur, self.current_level.entitySprite)
                        if selecting != None:
                            for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                                item.destroy()
                                
                            for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                                item.destroy()
                            
                            selecting.drawAction(self) # Dessin de la nouvelle Frame
                            self.currentSelected = (selecting, selecting.__class__.__name__)
                            
                ### Event timer ###
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
                            self.current_level.ressource[producer.name] += 1
                            if producer.currentRessource != 0:
                                producer.currentRessource -= 1
                                if self.currentSelected == None:
                                    for item in self.action.winfo_children(): # Destruction de l intérieur de la frame action
                                        item.destroy()
                                        
                                    for item in self.select.winfo_children(): # Destruction de l intérieur de la frame select
                                        item.destroy()
                                    producer.drawAction(self)
                            else:
                                self.current_level.ressourceSprite.remove(producer)
                    
                if event.type == USEREVENT  + 3: #Toute les secondes
                    for static in self.current_level.staticSprite:
                        for make in static.makeProduct:
                            self.current_level.ressource[make] += static.makeProduct[make]
                        for need in static.needProduct:
                            self.current_level.ressource[need] -= static.needProduct[need]
                            
  
                            
                        
                        
                for objet in self.current_level.movingSprite:
                    pos = pygame.mouse.get_pos()
                    objet.move((int(pos[0]/10), int(pos[1]/10)))
                    wrongWall = pygame.sprite.spritecollideany(objet, self.current_level.wallSpriteColide)
                    wrongBuild = pygame.sprite.spritecollideany(objet, self.current_level.staticSprite)
                    wrongEntity = pygame.sprite.spritecollideany(objet, self.current_level.entitySprite)
                    wrongRessource = pygame.sprite.spritecollideany(objet, self.current_level.ressourceSprite)
                    if wrongWall != None or wrongBuild != None or wrongEntity != None or wrongRessource != None:
                        pass
                    else:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.current_level.movingSprite.remove(objet)
                            self.current_level.staticSprite.add(objet)
                            if str(objet.__class__.__name__) == "home":
                                self.v = villageoi(self.current_level, (objet.positionX+1, objet.positionY+1))
                                self.current_level.entitySprite.add(self.v)
                                        
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
                colisioned = pygame.sprite.spritecollideany(colisioneur, self.current_level.staticSprite)
                if colisioned != None:
                    wall.append((x, y))
        map = myIA.GridWithWeights(constants.TAILLE_FENETRE[0],constants.TAILLE_FENETRE[1])
        map.walls = wall
        cfrom, sfar = myIA.a_star_search(map, currentPos, goal)
        path = myIA.reconstruct_path(cfrom, currentPos, goal)
        return path
    
    def mSave(self):
        self.saveName = self.user + "-" + str(datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%y-%H-%M-%S")) 
        conn = sqlite3.connect("DataBase/"+self.saveName+".db3")
        c = conn.cursor()
        cLevel = self.current_level.__class__.__name__
        ### Creation de la table
        c.execute("CREATE TABLE Level(ID integer not null unique primary key asc autoincrement,CurrentLevel TEXT);")
        c.execute("CREATE TABLE StaticSprite(ID integer not null unique primary key asc autoincrement,ClassName TEXT,Position TEXT,IDLevel REFERENCES Level);")
        c.execute("CREATE TABLE EntitySprite(ID integer not null unique primary key asc autoincrement,ClassName TEXT,Position TEXT,IDLevel REFERENCES Level);")
        c.execute("CREATE TABLE RessourceSprite(ID integer not null unique primary key asc autoincrement,ClassName TEXT,Position TEXT,IDLevel REFERENCES Level);")
        c.execute("CREATE TABLE Ressource(ID integer not null unique primary key asc autoincrement, RessourceName TEXT, NbRessource integer, IDLevel REFERENCES Level);")
        
        c.execute("INSERT INTO Level (CurrentLevel) VALUES (?);", (str(cLevel),))
        ### Entree des donnée
        for objet in self.current_level.staticSprite:
            className = objet.type
            position = str((objet.positionX, objet.positionY))
            c.execute("INSERT INTO StaticSprite (ClassName, Position, IDLevel) VALUES (?, ?, (SELECT ID FROM Level where CurrentLevel = (?)));", (className, position, str(cLevel)))
        
        for objet in self.current_level.entitySprite:
            className = objet.__class__.__name__
            position = str((objet.positionX, objet.positionY))
            c.execute("INSERT INTO EntitySprite (className, Position, IDLevel) VALUES (?, ?, (select ID from Level where CurrentLevel = (?)));", (className, position, str(cLevel)))

        for objet in self.current_level.ressourceSprite:
            className = objet.name
            position = str((objet.positionX, objet.positionY))
            c.execute("INSERT INTO RessourceSprite (className, Position, IDLevel) VALUES (?, ?, (select ID from Level where CurrentLevel = (?)));", (className, position, str(cLevel)))
        
        for ressource in self.current_level.ressource:
            c.execute("INSERT INTO Ressource (RessourceName, NbRessource, IDLevel) VALUES (?, ?, (select ID from Level where CurrentLevel = (?)));", (ressource, self.current_level.ressource[ressource], str(cLevel)))
        conn.commit()
        c.close()
        
        conn = sqlite3.connect("DataBase/UserData.db3")
        c = conn.cursor()
        
        c.execute("INSERT INTO UserSave (Save, UserID) Values (?, (select ID from User where Name = (?)));", (self.saveName, self.user))
        
        conn.commit()
        c.close()
    
    def backToMainMenu(self):
        self.game.destroy()
        os.system('mainMenu.py')

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
        self.staticSprite.draw(screen)
        self.ressourceSprite.draw(screen)
        self.entitySprite.draw(screen)
        self.movingSprite.draw(screen)
        
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
            [ (12, 12),"Wood"],
            [ (13, 14),"Wood"],
            [ (16, 15),"Wood"],
            [ (25, 19),"Wood"],
            [ (20, 30),"Stone"],
            [ (23, 28),"Stone"],
            [ (17, 33),"Stone"],
            [ (30, 45),"Food"],
            [ (33, 42),"Food"]
        ]
        
        for provides in levelRessource:
            x = ressource(self, provides[0], provides[1])
            self.ressourceSprite.add(x)
                    
        #self.home1 = home(self, (5,5))
        #self.staticSprite.add(self.home1)
        #self.villageoi1 = villageoi(self, (6,6))
        #self.entitySprite.add(self.villageoi1)
        
        #self.home2 = home(self, (8, 6))
        #self.staticSprite.add(self.home2)
        self.villageoi2 = villageoi(self, (9, 7))
        self.entitySprite.add(self.villageoi2)

            
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
        
### Class de touts les batiment et leur fonctionnement
class build(entity):
    def __init__(self,level, position, type, cost={}, need={}, make={}):
        entity.__init__(self, level, position)
        self.type = type
        self.cost = cost
        self.needProduct = need
        self.makeProduct = make
        self.loadImg("image/"+self.type+".png", position)

    def drawAction(self, fen):
        self.buildNameLabel = Label(fen.select, text=self.type)
        self.buildNameLabel.grid()

### class de touts les ressources et leur fonctionnement
class ressource(entity):
    def __init__(self, level, position, name):
        entity.__init__(self, level, position)
        self.currentRessource = 300
        self.ressource = 300
        self.name = name
        self.loadImg("image/"+self.name+".png", position)
        level.ressource[self.name] = 100
    
    def drawAction(self, fen):
        self.nameRessouceLabel = Label(fen.select, text=self.name)
        self.nameRessouceLabel.grid()

        self.ressourceLabel = Label(fen.select, text="Ressource :")
        self.ressourceLabel.grid(row=1, column=0)

        self.currentRessourceLabel = Label(fen.select, text=self.currentRessource)
        self.currentRessourceLabel.grid(row=1, column=1)
        
class villageoi(entity):
    def __init__(self, level, position):
        entity.__init__(self, level, position)
        self.vie = 30
        self.vieMax = 30
        self.loadImg("image/Character.png", position)
        self.moveActive = False
        
    def drawAction(self, fen):
        # Frame Action 
        comptoireButton = Button(fen.action, text="Town Center (Wood: 250, Stone: 100)", command= lambda: self.building("TownCenter", {"Wood": 250, "Stone": 100}))
        comptoireButton.grid(row=0)
               
        woodFarmButton = Button(fen.action, text="House (Wood: 30)", command= lambda: self.building("House", {"Wood": 30}))
        woodFarmButton.grid(row=1)
        
        wheatFarmButton = Button(fen.action, text="Lumber Camp (Wood: 100)", command= lambda: self.building("LumberCamp", {"Wood": 100},{}, {"Wood":1}))
        wheatFarmButton.grid(row=2)
        
        cobleFarmButton = Button(fen.action, text="Mining Camp (Wood: 100)", command= lambda: self.building("MiningCamp", {"Wood": 100}, {}, {"Stone":1}))
        cobleFarmButton.grid(row=3)
        
        homeButton = Button(fen.action, text="Farm (Wood: 60)", command= lambda: self.building("Farm", {"Wood": 60},{}, {"Food":1}))
        homeButton.grid(row=4)
        
        # Frame Select        
        VieLabel = Label(fen.select, text=self.vie)
        VieMaxLabel = Label(fen.select, text=self.vieMax)
        VieLabel.grid(row=0, column=0)
        VieMaxLabel.grid(row=0, column=1)
        
    def moveEntity(self):
        self.moveActive = True
    
    def building(self, type, cost={}, need={}, make={}):
        x = build(self.currentLevel, (10,10), type, cost, need, make)

        validator = True
        for price in x.cost:
            if self.currentLevel.ressource[price] - x.cost[price] < 0:
                validator = False
        if validator:
            for price in x.cost:
                self.currentLevel.ressource[price] -= x.cost[price]
            self.currentLevel.movingSprite.add(x)

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
                
if __name__ == "__main__":
    x = main("moi")