import pygame
import time
pygame.init()

class Player():

    def __init__(self):
        self.Name = ""
        self.Score = 0
        self.GameMode = ""
        self.Board = None
        self.GameDifficulty = ""
        self.CurrentMenu = ""
# Used in Save Game to store Player details  

class SetUp:
    border_x = 605
    border_y = 600
    Display = pygame.display.set_mode((border_x,border_y))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Game")
# Sets the screen for the game

class Colour:
    white = (255,255,255)
    black = (0,0,0)
    lightgrey  = (131,139,139)
    grey = (193,205,205)
# colours used through the game

class Images:
    WoodenBlockH = pygame.image.load("WoodenBlockH.png")
    WoodenBlockV = pygame.image.load("WoodenBlockV.png")
    WoodenBlockHL = pygame.image.load("woodenblockhl.png")
    WoodenBlockVL = pygame.image.load("woodenblockvl.png")
    EscapeBlock = pygame.image.load("EscapeBlock.png")
    Background = pygame.image.load("Background.png")
    Instructions = pygame.image.load("Instructions.png")
# images loaded to be used as background and blocks

class Font:
    pygame.font.init()
    font = pygame.font.SysFont(None, 25)
# font initialisation

class Utility: 
    def MergeSort(ArrayToSort):
        if len(ArrayToSort)>1:
            mid = len(ArrayToSort) // 2
            lefthalf = ArrayToSort[:mid]
            righthalf = ArrayToSort[mid:]

            Utility.MergeSort(lefthalf)
            Utility.MergeSort(righthalf)

            i=0
            j=0
            k=0
            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i][1] < righthalf[j][1]:
                    ArrayToSort[k]=lefthalf[i]
                    i=i+1
                else:
                    ArrayToSort[k]=righthalf[j]
                    j=j+1
                k=k+1

            while i < len(lefthalf):
                ArrayToSort[k]=lefthalf[i]
                i=i+1
                k=k+1

            while j < len(righthalf):
                ArrayToSort[k]=righthalf[j]
                j=j+1
                k=k+1
    # used to sort scores

    def Star(x,y): # uses lines to draw a star from its top
        pygame.draw.aaline(SetUp.Display,Colour.black,[x, y + 50],[x + 50, y + 50],True)
        pygame.draw.aaline(SetUp.Display,Colour.black,[x + 50, y + 50],[x + 5, y + 70],True)
        pygame.draw.aaline(SetUp.Display,Colour.black,[x + 5, y + 70],[x + 25, y + 45],True)
        pygame.draw.aaline(SetUp.Display,Colour.black,[x + 25, y + 45],[x + 45, y + 70],True)
        pygame.draw.aaline(SetUp.Display,Colour.black,[x, y + 50],[x + 45, y + 70],True)
        pygame.display.update()
    
