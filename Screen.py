import pygame
import pickle
import Settings

class Screen:
    def __init__(self, player:Settings.Player):
        self.player = player

    def StartScreen(self): # Displays Start screen at the beginning of game
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("Escape", Settings.Colour.black, 125, 50, 150) # title
        self.__messagee("Block", Settings.Colour.black, 200, 200, 125) # title
        while self.player.CurrentMenu == "StartScreen": # updates settings
            for event in pygame.event.get(): # menu screen buttons ; last parameter is the next screen
                self.__button("Main Menu", 250, 325, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "MainMenu")
                self.__button("Instructions", 250, 400, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "Instructions")
                self.__button("Score Table", 250, 475, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "ScoreTable")
                pygame.display.update() # updates window

    def MainMenu(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("Main Menu", Settings.Colour.black, 125, 50, 95) # title
        while self.player.CurrentMenu == "MainMenu": # updates settings
            for event in pygame.event.get():# screen buttons ; last parameter is the next screen
                self.__button("Arcade", 250, 200, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "DifficultySelect")
                self.__button("Time Trial", 250, 300, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "DifficultySelect")
                self.__button("LoadGame", 250, 400, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "LoadScreen")
                self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                pygame.display.update()

    def Instructions(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("Instructions", Settings.Colour.black, 50, 50, 95) # title
        while self.player.CurrentMenu == "Instructions": # updates settings
            for event in pygame.event.get():# screen buttons ; last parameter is the next screen
                Settings.SetUp.Display.blit(Settings.Images.Instructions, [0,0]) # loads image on screen from file
                self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                pygame.display.update()

    def DifficultySelect(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("Difficulty Select", Settings.Colour.black, 50, 50, 95) # title
        while self.player.CurrentMenu == "DifficultySelect": # updates settings
            for event in pygame.event.get():# screen buttons ; last parameter is the next screen
                self.__button("Easy", 250, 250, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "7")
                self.__button("Medium", 250, 350, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "8")
                self.__button("Hard", 250, 450, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "9")
                self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                pygame.display.update()

    def SaveScreen(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("SaveScreen", Settings.Colour.black, 40, 50, 95) # title
        while self.player.CurrentMenu == "SaveScreen": # updates settings
            for event in pygame.event.get():# screen buttons ; last parameter is the next screen
                self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                self.__Write_To_Screen(self.player.Board) # allows user to type on screen
                pygame.display.update()

    def LoadScreen(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("Game Select", Settings.Colour.black, 50, 50, 95) # title
        file = open("SavedNames.txt","rb")
        Arr = []
        try:
            while True:
                Obj = pickle.load(file) # loads contents from memory
                Num = pickle.load(file)
                Arr.append(Obj + ".txt")
        except:
            print()
        while self.player.CurrentMenu == "LoadScreen": # updates settings
            pygame.event.get()
            self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "MainMenu")
            self.__SavedList(Arr)
            pygame.display.update()
    # loads saved games 

    def ScoreTable(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        self.__messagee("Score Table", Settings.Colour.black, 50, 50, 95) # title
        file = open("SavedNames.txt","rb")
        Arr = []
        try:
            while True:
                Obj = pickle.load(file) # loads contents from memory
                Num = pickle.load(file)
                Arr.append([Obj,Num])
        except:
            print()
        x = 50
        y = 200
        Settings.Utility.MergeSort(Arr) # sorts scores
        for Person in Arr:
            String = ""
            String = String + Person[0]
            String = String + " "
            String = String + str(Person[1])
            self.__messagee(String, Settings.Colour.black, x, y, 25) # prints scores on screen
            if y == 500:
                x = x + 100
            y = y + 100
        while self.player.CurrentMenu == "ScoreTable": # updates settings
            pygame.event.get()# screen buttons ; last parameter is the next screen
            self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
            pygame.display.update()
    # loads contents from binary file and performs a mergesort

    def LevelComplete(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        while self.player.CurrentMenu == "LevelComplete" : # updates settings
            for event in pygame.event.get():# screen buttons ; last parameter is the next screen
                self.__messagee("Level Complete", Settings.Colour.black, 40, 50, 100)
                self.__messagee("Moves : " + str(self.player.Score), Settings.Colour.black, 200, 200, 50)
                self.__button("SaveGame", 225, 400, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "SaveScreen")
                if self.player.Score < 7:
                    Settings.Utility.Star(200,250)
                    Settings.Utility.Star(250,250)
                    Settings.Utility.Star(300,250)
                elif 7 <= self.player.Score <= 9:
                    Settings.Utility.Star(225,250)
                    Settings.Utility.Star(275,250)
                elif 9 < self.player.Score:
                    Settings.Utility.Star(250,250)
                self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                pygame.display.update()

    def LevelFailed(self):
        Settings.SetUp.Display.fill(Settings.Colour.grey) # background
        while self.player.CurrentMenu == "LevelFailed" : # updates settings
            for event in pygame.event.get():# screen buttons ; last parameter is the next screen
                self.__messagee("Level Failed", Settings.Colour.black, 40, 50, 100)
                self.__messagee("Better Luck Next Time", Settings.Colour.black, 100, 200, 50)
                self.__button("Retry", 225, 400, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                self.__button("<-", 0, 550, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "StartScreen")
                pygame.display.update()
                
# class used for buttons and screen rendering
#class self:
    def __button(self, text, x, y, width, height, inactive, active, subroutine):
        self.__ButtonText(text, Settings.Colour.black, x, y, width, height)
        cur = pygame.mouse.get_pos() # gets mouse position
        click = pygame.mouse.get_pressed() # gets click
        if x + width > cur[0] > x and y + height > cur[1] > y:  # checks position of mouse 
            pygame.draw.rect(Settings.SetUp.Display, active, [x,y,width,height]) # creates button
            self.__ButtonText(text, Settings.Colour.black, x, y, width, height) # prints text onto screen
            if click[0] == 1:
                if text == "Time Trial":
                    self.player.GameMode = self.player.GameMode + "TimeTrial"
                if text == "Easy" or text == "Medium" or text == "Hard":
                    self.player.GameDifficulty = subroutine
                    self.player.CurrentMenu = ""
                else:
                    self.player.CurrentMenu = subroutine
        else:
            pygame.draw.rect(Settings.SetUp.Display, inactive, [x,y,width,height])
            self.__ButtonText(text, Settings.Colour.black, x, y, width, height)
    # loads a button while the cursor is above the mouse the button will change colour
    # used to navigate between interfaces

    def __SavedList(self, List):
        x = 50
        y = 200
        for name in List:
            pygame.event.get() # displays list as 3x5 collunms 
            self.__button(name, x, y, 100, 50, Settings.Colour.grey, Settings.Colour.lightgrey, "LoadGame")
            if y == 500:
                x = x + 100
            y = y + 100
            pygame.display.update()
    # used to display scores

    def __Write_To_Screen(self, Board):
        font = pygame.font.Font(None, 50)
        pygame.draw.rect(Settings.SetUp.Display,Settings.Colour.white,[250,200,100,50],0) 
        self.__ButtonText(self.player.Name, Settings.Colour.black, 250, 200, 100, 50)
        pygame.display.update() # creates box
        while self.player.CurrentMenu == "SaveScreen":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha(): # if input is text
                        self.player.Name += event.unicode # update screen
                    elif event.key == pygame.K_BACKSPACE: # if backspace
                        self.player.Name = self.player.Name[:-1] # remove last item
                    elif event.key == pygame.K_KP_ENTER:
                        self.player.CurrentMenu = "StartScreen" # when finiched update setting
                pygame.draw.rect(Settings.SetUp.Display,Settings.Colour.white,[250,200,100,50],0)
                self.__ButtonText(self.player.Name, Settings.Colour.black, 250, 200, 100, 50)
                pygame.display.update()
    # allows a user to see what they are inputing as it is displayed onscreen
    # used for name input in SaveGame
    
    def __messagee(self, txt, colour, x, y, size):
        pygame.font.init() # initializes font module
        font = pygame.font.SysFont(None, size)  # gets font
        text = font.render(txt, True, colour)
        Settings.SetUp.Display.blit(text,[x,y]) # prints text
        pygame.display.update()
    # used for titles and screen messages by the programer

    def __ButtonText(self, message, colour, x, y, width, height, size ="small"):
        textSurf, textRect = self.__text_objects(message, colour, size) # puts message on screen
        textRect.center = (x+(width/2) , y+(height/2)) # gets centre of button
        Settings.SetUp.Display.blit(textSurf, textRect)
    # used to centre text on any rectangular onject

    def __text_objects(self, text, colour, size):
        font = pygame.font.SysFont(None, 25) # gets system font and size
        textSurface = font.render(text, True, colour) 
        return textSurface, textSurface.get_rect()
    # used to render font
