from bridgeFunction import *

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
        
        if color == 1: 
            self.image = pygame.image.load(PATH+'black.png')
        elif color == -1:
            self.image = pygame.image.load(PATH+'white.png')
 
        self.image = pygame.transform.scale(self.image, (70,70))
        self.rect = self.image.get_rect()
        

    def draw(self, screen,pixel):
        self.rect.center = (pixel[0],pixel[1])
        screen.blit(self.image,self.rect)
        



