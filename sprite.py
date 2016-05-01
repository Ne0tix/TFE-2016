import pygame

class sprite(pygame.sprite.Sprite):

    def __init__(self, imageData, screen):
        pygame.sprite.Sprite.__init__(self)
        self.spriteSheet = pygame.image.load(imageData).convert()
        self.rect = self.spriteSheet.get_rect()
        
        
    