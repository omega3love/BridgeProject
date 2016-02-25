import pygame, sys
from pygame.locals import *
from batoosprites import *
from batoo import *

def Main():
  
  size = ( 11, 11 )
  tileSize = 50
  screen_size = ( (size[0]+1)*tileSize, (size[1]+1)*tileSize )

  board = Board(size, tileSize)
  board.rect.center = ( screen_size[0]/2, screen_size[1]/2 )
  pl = placement()
  '''
  all_stones = pygame.sprite.Group()
  for i in range(1, size[0]+1):
    for j in range(1, size[1]+1):
      sb = Stone(BLACK, tileSize, (i, j))
      sw = Stone(WHITE, tileSize, (i, j))
      all_stones.add(sb, sw)
  '''

  cursor_mark = Cursor_Marking(tileSize)
  turn = 1 # odd for black, even for white

  pygame.init()
  screen = pygame.display.set_mode(screen_size)
  clock  = pygame.time.Clock()
  fps = 30

  while True:

    color = current_color(turn)

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONUP:
        mouse = pygame.mouse.get_pos()
        markable = cursor_marking(mouse, size, tileSize, 1)
        if markable:
          if pl.is_placable(markable, color):
            pl.history.append( [markable, color, 1] )
            catchable = pl.is_catching(markable, color)
            if catchable:
              for caught in catchable:
                for stone in pl.history:
                  if stone[0] == caught and stone[-1] == 1:
                    stone[-1] = 0
            turn += 1

    screen.fill(WHITE)

    board.draw(screen)

    #---------- Mouse Cursor Marking ----------#
    mouse = pygame.mouse.get_pos()
    markable = cursor_marking(mouse, size, tileSize, 1)
    if markable:
      if pl.is_placable(markable, color):
        cursor_mark.draw(screen, markable)
    #------------------------------------------#
    
    #---------- Drawing Live Stones -----------#
    for stones in pl.history:
      if stones[-1] == 1:
        pos = grid_to_rectcenter(stones[0], tileSize)
        Stone(stones[1], tileSize, stones[0]).draw(screen, pos)
    #------------------------------------------#
    
    #pygame.time.wait(500)
    #print pl.history
    pygame.display.update()
    clock.tick(fps)


def cursor_marking(mouse, screenSize, tileSize, gridReturn = 0):

  cursor_range = tileSize/2
  for i in range(1, screenSize[0]+1):
    for j in range(1, screenSize[1]+1):
      x_range = ( i*tileSize - cursor_range, i*tileSize + cursor_range )
      y_range = ( j*tileSize - cursor_range, j*tileSize + cursor_range )
      if x_range[0] < mouse[0] <= x_range[1]:
        if y_range[0] < mouse[1] <= y_range[1]:
          if gridReturn:
            return (i, j)
          else:
            return (i*tileSize, j*tileSize)

  return False

def current_color(turn):

  if turn % 2 == 0:
    return WHITE
  else:
    return BLACK
          
def grid_to_rectcenter(grid, tileSize):

  return (grid[0]*tileSize, grid[1]*tileSize)


##################################

if __name__ == '__main__':
  Main()
