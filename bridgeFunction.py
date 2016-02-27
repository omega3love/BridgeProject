import pygame
import math
from bridgeMain import *

#Description
#Convert Grid (0,0) ~ (6,6) to Relative Pixel Position about the center

def GridToPixel(col, row):
    if col>0 and col<girdSize and row>0 and row<girdSize:
        pixelY = 60*(col-4)+30
        pixelX = 60*(row-4)+30
        return (pixelX,pixelY)

#Description
#Inverse function of GridToPixel Function

def PixelToGrid(pixelX, pixelY):
    col = pixelY/60+4
    row = pixelX/60+4
    return (col,row)
    


