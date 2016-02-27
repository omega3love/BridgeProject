import pygame
import math
from bridgeMain import *
from bridgeFunction import *
from colors import *

PATH = './drawing/'

######################################################################
# Board Class
######################################################################
class Board(pygame.sprite.Sprite):    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(PATH+'rawboard.png')
        self.image = pygame.transform.scale(self.image, (360,360))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = (screenWidth/2,screenHeight/2)
        screen.blit(self.image,self.rect)

######################################################################
# Stone Class
######################################################################

class Stone(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        
        if color == WHITE: 
            self.image = pygame.image.load(PATH+'whiteShip.png')
        else:
            self.image = pygame.image.load(PATH+'blackShip.png')
 
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (45,45))


    def draw(self, screen):
        return



