import pygame
from colors import *

PATH = './drawing/'


class Board(pygame.sprite.Sprite):    
    def __init__(self, size=(6,6)):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.image.load(PATH+'board.png')
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = (400,400)
        screen.blit(self.image,self.rect)

class Ship(pygame.sprite.Sprite):
    def __init__(self, color, grid):
        pygame.sprite.Sprite.__init__(self)
        
        if color == WHITE: 
            self.image = pygame.image.load(PATH+'whiteShip.png')
        else:
            self.image = pygame.image.load(PATH+'blackShip.png')
 
        self.rect = self.image.get_rect()
'''
    def draw(self, screen):
        ###--- Need to place ship on right place---###
'''
