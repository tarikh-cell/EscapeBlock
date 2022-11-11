import pygame
import time
import random
import pickle
import Settings
import Screen

pygame.init()


# class that defines block and has subroutines on the manipulation of blocks
class Block:
    def __init__(self, image, Orientation: str, x: int, y: int, width: int, height: int):
        self.image = image  # image loaded in from file
        self.Orientation = Orientation
        self.x = x  # coordinates are taken from the top left of a block
        self.y = y
        self.width = width
        self.height = height

    # all the attributes a block will have

    def X(self):
        return range(self.x, self.x + self.width)

    # used to return the range of x coordinates a block covers for collision detection

    def Y(self):
        return range(self.y, self.y + self.height)

    # used to return the range of y coordinates a block covers for collision detection

    def MoveBlock(self, Blocks):
        global EscapeBlock, EscapeBlock
        if self.Orientation == "H":
            while Blocks.player.CurrentMenu == "":
                Blocks.CountDown()  # used for Time Trial
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if self.CollisionD(-100, 0, Blocks):  # collision check
                                self.x = self.x - self.height  # moves block left
                        elif event.key == pygame.K_RIGHT:
                            if self.CollisionD(100, 0, Blocks):  # collision check
                                self.x = self.x + self.height  # moves block right
                        elif event.key == pygame.K_h:
                            Blocks.GenerateNewBlocks()
                        Blocks.player.Score = Blocks.player.Score + 1
                        Blocks.BlitBlock()  # updates screen
                    Blocks.SelectBlock()  # checks if another block has been selected
        elif self.Orientation == "V":
            while Blocks.player.CurrentMenu == "":
                Blocks.CountDown()  # used for Time Trial
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if self.CollisionD(0, -100, Blocks):  # collision check
                                self.y = self.y - self.width  # moves block down
                        elif event.key == pygame.K_DOWN:
                            if self.CollisionD(0, 100, Blocks):  # collision check
                                self.y = self.y + self.width  # moves block up
                        elif event.key == pygame.K_h:
                            Blocks.GenerateNewBlocks()
                        Blocks.player.Score = Blocks.player.Score + 1
                        Blocks.BlitBlock()  # updates screen
                    Blocks.SelectBlock()  # checks if another block has been selected

    # uses collision detection so blocks do not collide
    # block movement is only allowed within its orientation
    # will only move one block at a time

    def CollisionD(self, x: int, y: int, Blocks):
        self.x = self.x + x  # moves block to new position
        self.y = self.y + y
        if self._Boarder() == False:  # if new position moves block out of bounds -
            self.x = self.x - x  # reset block position -
            self.y = self.y - y  # then collision is false
            return False
        a = set(self.X())  # a set of all the x coordinates of the block is taken
        b = set(self.Y())
        for block in Blocks.board:
            if block != self:
                if a.intersection(block.X()) and b.intersection(block.Y()):
                    self.x = self.x - x  # if any points intersect between two -
                    self.y = self.y - y  # blocks then collision is false
                    return False
        self.x = self.x - x  # if no collision blocks can move
        self.y = self.y - y
        return True

    # takes the range of coordinates a block covers
    # loops through all blocks in the game
    # then does not allow movement if it collides

    def _Boarder(self):
        if 0 > self.y or self.y + self.height > 600:
            return False  # checks if block will leave game window
        if 0 > self.x or self.x + self.width > 600:
            return False
            # makes sure while a block is being moved it does not leave the screen


class SubBlockClass(Block):
    def __init__(self, image, Orientation, x, y, width, height, Direction1, Direction2, Identifier, TriedToMove):
        super().__init__(image, Orientation, x, y, width, height)
        self.__Direction1 = Direction1  # first direction to be traversed
        self.__Direction2 = Direction2  # second direction to be traversed
        self.__Identifier = Identifier  # integer to identify blocks
        self.__TriedToMove = TriedToMove  # Boolean to check if a block has moved

    def Hint(self, Blocks):
        for block in Blocks.board:
            if block.y == 200 and block.Orientation == "H":
                EscapeBlock = block
        try:
            while EscapeBlock.x != 400:
                EscapeBlock.DepthFirstSearch(EscapeBlock, Blocks)  # gives hint
                EscapeBlock.Direction2 = "Right"
        except:
            pass
    def DepthFirstSearch(self, EscapeBlock, Board):
        if EscapeBlock.x == 400:  # base case
            print()
        else:
            if self.__TriedToMove == True:  # if a block has been moved then try -
                self.__Direction1 = self.__Direction2  # move in opposite direction
            ThisBlockCanMove, ObstructingBlock, Boarder = self.CheckEmpty(self.__Direction1, Board)
            if ThisBlockCanMove == False:  # if block can not be moved
                if Boarder == "Boarder Reached":  # if boarder reached -
                    self.__Direction1 = self.__Direction2  # move in opposite direction
                    return "Boarder Reached"
                else:
                    Done = ObstructingBlock.DepthFirstSearch(EscapeBlock, Board)
                    # try to move block that is blocking current bllock
        self.__TriedToMove = True
        return ""

    def CheckEmpty(self, Direction: str, Board):
        if Direction == "Right":
            Boolean, Block, Boarder = self.ColissionD(100, 0, Board)
            while Boolean:
                self.x = self.x + 100  # move as far as possible -
                self.BlitBlocks(Board)  # without colliding
                Boolean, Block, Boarder = self.ColissionD(100, 0, Board)
            return Boolean, Block, Boarder  # return block that is blocking path
        elif Direction == "Left":
            Boolean, Block, Boarder = self.ColissionD(-100, 0, Board)
            while Boolean:
                self.x = self.x - 100  # move as far as possible -
                self.BlitBlocks(Board)  # without colliding
                Boolean, Block, Boarder = self.ColissionD(-100, 0, Board)
            return Boolean, Block, Boarder  # return block that is blocking path
        elif Direction == "Up":
            Boolean, Block, Boarder = self.ColissionD(0, 100, Board)
            while Boolean:
                self.y = self.y + 100  # move as far as possible -
                self.BlitBlocks(Board)  # without colliding
                Boolean, Block, Boarder = self.ColissionD(0, 100, Board)
            return Boolean, Block, Boarder  # return block that is blocking path
        elif Direction == "Down":
            Boolean, Block, Boarder = self.ColissionD(0, -100, Board)
            while Boolean:
                self.y = self.y - 100  # move as far as possible -
                self.BlitBlocks(Board)  # without colliding
                Boolean, Block, Boarder = self.ColissionD(0, -100, Board)
            return Boolean, Block, Boarder  # return block that is blocking path

    def ColissionD(self, x: int, y: int, Board):
        self.x = self.x + x  # method over ride
        self.y = self.y + y  # will return block that is blocking path
        if self._Boarder() == False:  # unlike original method
            self.x = self.x - x
            self.y = self.y - y
            return False, self, "Boarder Reached"
        a = set(self.X())
        b = set(self.Y())
        for block in Board.board:
            if block != self:
                if a.intersection(block.X()) and b.intersection(block.Y()):
                    self.x = self.x - x
                    self.y = self.y - y
                    return False, block, ""
        self.x = self.x - x
        self.y = self.y - y
        return True, self, ""
        # takes the range of coordinates a block covers
        # loops through all blocks in the game
        # then does not allow movement if it collides

    def BlitBlocks(self, Blocks):
        Settings.SetUp.Display.blit(Settings.Images.Background, [0, 0])
        for Block in Blocks.board:
            Settings.SetUp.Display.blit(Block.image, [Block.x, Block.y])
        pygame.display.update()

# class that creates the board and manipulates it
class Board:
    def __init__(self, board, timer: float, player):
        self.board = []  # list of blocks
        self.__timer = 30
        self.player = player
        EscapeB = Block(Settings.Images.EscapeBlock, "H", 400, 200, 200, 100)
        self.board.append(EscapeB)  # creates escape block
        BlockOri = ["H", "V", "V"]  # different orientations a block can have
        BlockLength = [200, 200, 300]  # fifferent lengths a block can have
        for x in range(0, int(player.GameDifficulty)):
            print(x)
            Orientation = random.choice(BlockOri)  # random orientation
            Length = random.choice(BlockLength)  # random length
            if Orientation == "H":
                if Length == 200:  # block instanciation
                    block = Block(Settings.Images.WoodenBlockH, "H", 0, 0, 200, 100)
                else:
                    block = Block(Settings.Images.WoodenBlockHL, "H", 0, 0, 300, 100)
                self.__PositionBlock(block)  # gives block x and y coordinates
                self.board.append(block)
            elif Orientation == "V":
                if Length == 200:  # block instanciation
                    block = Block(Settings.Images.WoodenBlockV, "V", 0, 0, 100, 200)
                else:
                    block = Block(Settings.Images.WoodenBlockVL, "V", 0, 0, 100, 300)
                self.__PositionBlock(block)  # gives block x and y coordinates
                self.board.append(block)
        player.Board = self  # updates settings
        print("DONE")

    # randomly choses an orientation and width for blocks
    # the uses position block to place them
    # then instanciates board to be used in tyhe game


    def BlitBlock(self):
        Settings.SetUp.Display.blit(Settings.Images.Background, [0, 0])
        for Block in self.board:
            Settings.SetUp.Display.blit(Block.image, [Block.x, Block.y])
        pygame.display.update()

    # whenever a change is made is uesd to update the screen
    # first loads background then all the blocks on top of background

    def SelectBlock(self):
        self.CheckWin()  # check if level complete
        cur = pygame.mouse.get_pos()  # gets mouse position
        pygame.event.get()
        click = pygame.mouse.get_pressed()  # checks mouse click
        for ablock in self.board:
            if cur[0] in range(ablock.x, ablock.x + ablock.width) and cur[1] in range(ablock.y,
                                                                                      ablock.y + ablock.height):
                if click[0] == 1:
                    ablock.MoveBlock(self)  # if mouse is over a block and clicks
                    # return Block            then allow user to move block

    # uses the position of the mouse and left click to check if a block is in the vacinity
    # checks if the level is complete

    def SetUpEscapeB(self):
        recent = 0
        counter = 0
        for block in self.board:
            if block.Orientation == "H" and block.y == 200:
                EscapeB = block
        while EscapeB.x != 0:
            if counter == 15:
                board = []
                timer = 0
                Temp = Board(board, timer, player)
                self.board = Temp.board
                counter = 0
                for block in self.board:
                    if block.Orientation == "H" and block.y == 200:
                        EscapeB = block
            random.shuffle(self.board)
            for Block in self.board:
                while EscapeB.CollisionD(-100, 0, self):
                    EscapeB.x = EscapeB.x - 100
                    self.BlitBlock()
                if Block != EscapeB:
                    if Block.Orientation == "V":
                        if Block.CollisionD(0, 100, self):
                            while Block.CollisionD(0, 100, self):
                                Block.y = Block.y + 100
                                self.BlitBlock()
                                recent = Block
                        elif Block.CollisionD(0, -100, self):
                            while Block.CollisionD(0, -100, self):
                                Block.y = Block.y - 100
                                self.BlitBlock()
                                recent = Block
                    if Block.Orientation == "H":
                        if Block.CollisionD(100, 0, self):
                            while Block.CollisionD(100, 0, self):
                                Block.x = Block.x + 100
                                self.BlitBlock()
                                recent = Block
                        elif Block.CollisionD(-100, 0, self):
                            while Block.CollisionD(-100, 0, self):
                                Block.x = Block.x - 100
                                self.BlitBlock()
                                recent = Block
            counter = counter + 1

    # used to move the escape block from the exit to its starting poistion
    # makes sure there are no collisions
    # used to check if level is possible

    def ReShuffle(self):
        Ready = True
        while Ready:
            for Block in self.board:
                if Block != EscapeB:
                    if Block.Orientation == "H":
                        if Block.CollisionD(100, 0, self):
                            Block.x = Block.x + 100
                            self.BlitBlock()
                        elif Block.CollisionD(-100, 0, self):
                            Block.x = Block.x - 100
                            self.BlitBlock()
                    if Block.Orientation == "V":
                        if Block.y == 100 or Block.y == 200:
                            Ready = False
                        elif Block.CollisionD(0, 100, self):
                            Block.y = Block.y + 100
                            self.BlitBlock()
                        elif Block.CollisionD(0, -100, self):
                            Block.y = Block.y - 100
                            self.BlitBlock()

    # after escape block is positioned
    # used to block exit to make game more challenging

    def CheckWin(self):
        for block in self.board:  # checks if the escape block is at the exit
            if block.y == 200 and block.Orientation == "H":
                if block.x == 400:
                    self.player.GameMode = ""
                    self.player.CurrentMenu = "LevelComplete"
                    self.player.GameDifficulty = ""

    # checks if the escape block is at the exit
    # then prompts user to save game

    def CountDown(self):
        if self.player.GameMode == "TimeTrial":
            clock = pygame.time.Clock()
            dt = 0  # time difference
            txt = str(round(self.__timer, 2))
            self.BlitBlock()  # prints time on screen
            # Screen.UserScreen.messagee(txt,Settings.Colour.black,500,25,40)
            pygame.font.init()  # initializes font module
            font = pygame.font.SysFont(None, 40)  # gets font
            text = font.render(txt, True, Settings.Colour.black)
            Settings.SetUp.Display.blit(text, [500, 25])
            pygame.display.update()
            dt = clock.tick(30) / 1000
            self.__timer = self.__timer - dt  # updates time
            if self.__timer < 0:
                self.player.GameMode = ""
                self.player.CurrentMenu = "LevelFailed"
                self.player.GameDifficulty = ""

    # used as stopwatch in time trial

    def __BlankSpace(self):
        Empty = Block(None, None, 0, 0, 100, 100)  # one by one block
        Spaces = []  # Available coordinates
        for X in range(0, 6):
            Empty.x = X * 100  # range of x coordinates
            for Y in range(0, 6):
                Empty.y = Y * 100  # range of y coordinates
                if Empty.CollisionD(0, 0, self):
                    Spaces.append([Empty.x, Empty.y])
        return Spaces

    # used to search for vacant spaces for possible block movement
    # feeds a one by one block
    # checks if that position is empty

    def SaveGame(self):
        File = open(self.player.Name + ".txt", "wb")
        for block in self.board:
            if block.Orientation == "H" and block.y == 200:
                print("left out")  # escape block not saved
            else:
                pickle.dump([block.Orientation, block.x, block.y, block.width, block.height], File)
        File.close()
        File = open("SavedNames.txt", "ab")
        pickle.dump(self.player.Name, File)  # stores name
        pickle.dump(self.player.Score, File)  # stores score
        File.close()

    # used to save game

    def __PositionBlock(self, block):
        Available = self.__BlankSpace()  # gets a list of blank spaces
        if block.Orientation == "V":  # positions vertical blocks
            Position = random.choice(Available)
            block.x = Position[0]
            block.y = Position[1]
            while not block.CollisionD(0, 0, self):
                Position = random.choice(Available)
                block.x = Position[0]
                block.y = Position[1]
        if block.Orientation == "H":  # positions horizontal blocks
            Position = random.choice(Available)
            if Position[1] != 200:  # makes sure no block obstucts escape block
                block.x = Position[0]
                block.y = Position[1]
            while not block.CollisionD(0, 0, self):
                Position = random.choice(Available)
                if Position[1] != 200:
                    block.x = Position[0]
                    block.y = Position[1]
                    # creates board by placing blocks randomly across board

    def GenerateNewBlocks(self):
        NewBlocks = []
        ID = 0
        for block in self.board:
            if block.Orientation == "H":  # redefines blocks as part of subblockclass
                Newblock = SubBlockClass(block.image, "H", block.x, block.y, block.width, block.height, "Right", "Left",
                                         ID, False)
                NewBlocks.append(Newblock)
            elif block.Orientation == "V":
                Newblock = SubBlockClass(block.image, "V", block.x, block.y, block.width, block.height, "Up", "Down",
                                         ID, False)
                NewBlocks.append(Newblock)
            ID = ID + 1
        for Block in NewBlocks:
            if Block.Orientation == "H" and Block.y == 200:
                Block.Identifier = 100  # Escapeblock has identifier 100
                self.board = NewBlocks
                Block.Hint(self)

    # for every block a direction and identifier are given using the SubBlockClass

    def LoadGame(Title: str):
        File = open(Title, "rb")
        Arr = []
        try:
            while True:  # loads everything from memory
                Array = pickle.load(File)
                Arr.append(Array)
        except:
            File.close()
        blocks = []
        EscapeB = Block(Settings.Images.EscapeBlock, "H", 0, 200, 200, 100)
        blocks.append(EscapeB)
        for bloc in Arr:
            if bloc[0] == "V":
                if bloc[4] == 300:  # redefines objects as part of the block class
                    block = Block(Settings.Images.WoodenBlockVL, "V", bloc[1], bloc[2], 100, 300)
                else:
                    block = Block(Settings.Images.WoodenBlockV, "V", bloc[1], bloc[2], 100, 200)
                blocks.append(block)
            elif bloc[0] == "H":
                if bloc[3] == 300:
                    block = Block(Settings.Images.WoodenBlockHL, "H", bloc[1], bloc[2], 300, 100)
                else:
                    block = Block(Settings.Images.WoodenBlockH, "H", bloc[1], bloc[2], 200, 100)
                blocks.append(block)
                # Board = Board(blocks, 30,)
                # Board.BlitBlock()
                # run = True
                # while run:
                #   Board.SelectBlock()
                # used to load game


if __name__ == "__main__":
    player = Settings.Player() # instanciates player class
    theScreen = Screen.Screen(player) # used to track current screen 
    player.CurrentMenu = "StartScreen" # game starts at startscreen
    while True:
        if player.CurrentMenu != "": # checks for current screen
            if player.CurrentMenu == "StartScreen": # checks screen
                theScreen.StartScreen() # displays screen in settings module
            elif player.CurrentMenu == "MainMenu":
                theScreen.MainMenu()
            elif player.CurrentMenu == "Instructions":
                theScreen.Instructions()
            elif player.CurrentMenu == "DifficultySelect":
                theScreen.DifficultySelect()
            elif player.CurrentMenu == "SaveScreen":
                theScreen.SaveScreen()
                player.Board.SaveGame()
                player = Settings.Player()
                theScreen = Screen.Screen(player)
                player.CurrentMenu = "StartScreen"
            elif player.CurrentMenu == "LoadScreen":
                theScreen.LoadScreen()
            elif player.CurrentMenu == "ScoreTable":
                theScreen.ScoreTable()
            elif player.CurrentMenu == "LevelComplete":
                theScreen.LevelComplete()
            elif player.CurrentMenu == "LevelFailed":
                theScreen.LevelFailed()
        if player.GameDifficulty != "": # checks if a game has been selected
            board = [] # game board
            timer = 0 # time trial
            theBoard = Board(board, timer, player) # board instanciation
            theBoard.SetUpEscapeB() 
            while player.CurrentMenu == "": # stops when current menu is level complete
                theBoard.SelectBlock()  
