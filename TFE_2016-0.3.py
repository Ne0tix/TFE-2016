from tkinter import *
import pygame
import levels
import constants
import os

class main():    

    def __init__(self):
        self.game = Tk()
        
        # Frame Ressource
        self.ressource = Frame(self.game, width=100, height=480)
        self.ressource.grid(row=0, column=0)
        self.ressourceLabel = Label(self.ressource, text="Ressource").pack()
        
        # Frame Select
        self.select = Frame(self.game, width=100, height=150)
        self.select.grid(row=1, column=0)
        self.selectLabel = Label(self.select, text="Selection").pack()
        
        # Frame Action
        self.action = Frame(self.game, width=500, height=150)
        self.action.grid(row=1, column=1)
        self.selectLabel = Label(self.action, text="Action").pack()
        self.constructButton = Button(self.action, text="Construire",command=lambda: self.construct()).pack()
        
        # Frame Game
        self.embed = Frame(self.game, width=640, height=480)
        self.embed.grid(row=0, column=1)
        
            # Init de pygame dans la frame Game
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        pygame.display.init()
        self.screen = pygame.display.set_mode(constants.TAILLE_FENETRE)
        
        self.current_level = levels.Level01(self.screen)
        
        self.done = False
        
        self.clock = pygame.time.Clock()
        self.game.update()
        
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                

                    
            self.current_level.update()
            self.current_level.drawing(self.screen)
            self.clock.tick(60)
            pygame.display.flip()
            self.game.mainloop()
        pygame.quit()
    
    def construct(self):
        self.current_level.build("1.png")
    

if __name__ == "__main__":
    z = main()
    