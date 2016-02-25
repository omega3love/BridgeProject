import pygame
from batoocolors import *

PATH = './drawing/'
board_topleft = (0, 70)
board_tile_offset = 50
tileSize = 55

class Stone(pygame.sprite.Sprite):

    def __init__(self, color, grid, stone_type = 'normal'):

        # tileSize = 55 px
        self.color = color
        if type(color) == str:
            if color == "B":
                self.color = BLACK
            else:
                self.color = WHITE

        pygame.sprite.Sprite.__init__(self)
        '''
        offset = 5
        radius = tileSize / 2 - offset
        self.image = pygame.Surface((2 * radius, 2 * radius))
        self.image.fill(WHITE)
        '''

        if stone_type == 'normal': #1
            if self.color == WHITE:
                self.image = pygame.image.load(PATH + 'white.png')
            else:
                self.image = pygame.image.load(PATH + 'black.png')
        elif stone_type == 'hidden': #2
            if self.color == WHITE:
                self.image = pygame.image.load(PATH + 'white_hidden.png')
            else:
                self.image = pygame.image.load(PATH + 'black_hidden.png')
        elif stone_type == 'base': #3
            if self.color == WHITE:
                self.image = pygame.image.load(PATH + 'white_base.png')
            else:
                self.image = pygame.image.load(PATH + 'black_base.png')

        '''
        if self.color != WHITE:
            self.image.set_colorkey(WHITE)
            pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        else:
            pygame.draw.circle(self.image, BLACK, (radius, radius), radius, 1)
        self.radius = radius
        '''
        self.rect = self.image.get_rect()
        self.grid = grid

    def draw(self, screen):

        x = board_topleft[0] + (self.grid[0]-1)*tileSize + board_tile_offset
        y = board_topleft[1] + (self.grid[1]-1)*tileSize + board_tile_offset
        self.rect.center = (x, y)
        screen.blit(self.image, self.rect)


class Board(pygame.sprite.Sprite):

    def __init__(self, size=(11, 11)):

        pygame.sprite.Sprite.__init__(self)
        self.size = size  # (11, 11)
        '''
        offset = 0  # needs to display the edge line in self.image
        self.image = pygame.Surface(((size[0] - 1) * tileSize + offset, (size[1] - 1) * tileSize + offset))
        self.image.fill(WHITE)
        '''

        self.image = pygame.image.load(PATH + 'board.png')
        self.rect = self.image.get_rect()
        '''
        for col in range(size[0]):
            start_pos = col*tileSize, 0
            end_pos = col*tileSize, (size[1]-1)*tileSize
            pygame.draw.line(self.image, BLACK, start_pos, end_pos, 1)

        for row in range(size[1]):
            start_pos = 0, row*tileSize
            end_pos = (size[0]-1)*tileSize, row*tileSize
            pygame.draw.line(self.image, BLACK, start_pos, end_pos, 1)
        '''

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def project(self, map):

        self.image = pygame.image.load(PATH + 'board.png')
        offset = 40 # 50 - 10
        for p in map.plus:
            center = ( offset + (p[0]-1)*tileSize, offset + (p[1]-1)*tileSize )
            plus = pygame.image.load(PATH + 'plus.png')
            self.image.blit(plus, center)
        for m in map.minus:
            center = ( offset + (m[0]-1)*tileSize, offset + (m[1]-1)*tileSize )
            minus = pygame.image.load(PATH + 'minus.png')
            self.image.blit(minus, center)

        self.plus = map.plus
        self.minus = map.minus

class Cursor_Marking(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.size = tileSize / 2

        offset = 2  # wants to make it a bit smaller

        #self.image = pygame.Surface((self.size - offset, self.size - offset))
        #self.image.fill(BLACK)

        self.image = pygame.image.load(PATH + 'cursor.png')
        self.rect = self.image.get_rect()

    def draw(self, screen, pos):

        x = board_topleft[0] + (pos[0]-1)*tileSize + board_tile_offset
        y = board_topleft[1] + (pos[1]-1)*tileSize + board_tile_offset
        self.rect.center = (x, y)
        screen.blit(self.image, self.rect)

class Scoreboard(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(PATH + 'scoreboard.png')
        self.rect = self.image.get_rect()

    def draw(self, screen):

        screen.blit(self.image, self.rect)

