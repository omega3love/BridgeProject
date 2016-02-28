#! /usr/bin/python
import pygame
import math

""" Environment Variable """

screenWidth = 600
screenHeight = 600
gridSize = 6
screen = pygame.display.set_mode((screenWidth,screenHeight)) 
clock  = pygame.time.Clock() 
fps = 30 # frames per seconds


""" Color Definition """
WHITE = ( 255, 255, 255 )
BLACK = (   0,   0,   0 )
RED   = ( 255,   0,   0 )
GREEN = (   0, 255,   0 )
BLUE  = (   0,   0, 255 )
