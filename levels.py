import pygame
import constants
import sprite

class Level(object):
    staticSpriteColide = None
    movingSprite = None
    
    background = None
    
    def __init__(self):
        self.staticSpriteColide = pygame.sprite.Group()
        self.movingSprite = pygame.sprite.Group()
        
    def update(self):
        self.staticSpriteColide.update()
        self.movingSprite.update()
    
    def drawing(self, screen):
        screen.fill(constants.GREEN)
        screen.blit(self.background, (0,0))

        self.staticSpriteColide.draw(screen)
        self.movingSprite.draw(screen)
        
    def build(self, construct):
        self.build = sprite("1.png")
        self.movingSprite.add(self.build)
        
    def moveSprite(self, x,y):
        self.build.rect.x = x
        self.build.rect.y = y

class Level01(Level):
    def __init__(self, screen):
        Level.__init__(self)
        self.screen = screen
        
        self.background = pygame.image.load("Background.png").convert()
        self.background.set_colorkey(constants.GREEN)
        
        level = [ 
                ['Wall640.png', 0, 0],
                ["Wall640.png", 0, 470],
                ["wall480.png", 0, 0],
                ["wall480.png", 630, 0],
                ["Lac.png", 320, 240]
                ]
        for objet in level:
            block = sprite(objet[0])
            block.rect.x = objet[1]
            block.rect.y = objet[2]
            self.staticSpriteColide.add(block)
    
            
class sprite(pygame.sprite.Sprite):

    def __init__(self, imageData):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imageData).convert_alpha()
        self.rect = self.image.get_rect()
        
        
        