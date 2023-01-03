# implementation of card game - Memory
import sys
import pygame
import pygame.mouse
from pygame.locals import *
import random

pygame.init()

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

CARDWIDTH = 75
CARDHEIGHT = 100
WIDTH = CARDWIDTH * 17
HEIGHT = CARDHEIGHT

# Load images
CARD_BACK = pygame.image.load("Assets/CardBack.jpg")
CARD_BACK = pygame.transform.scale(CARD_BACK, (CARDWIDTH, CARDHEIGHT))
# CARD_BACK_WIDTH = 236
# CARD_BACK_HEIGHT = 355

ACE = pygame.image.load('Assets/AceDiamond.png')
ACE = pygame.transform.scale(ACE, (CARDWIDTH, CARDHEIGHT))
TWO = pygame.image.load('Assets/2Spade.png')
TWO = pygame.transform.scale(TWO, (CARDWIDTH, CARDHEIGHT))
THREE = pygame.image.load('Assets/3Heart.png')
THREE = pygame.transform.scale(THREE, (CARDWIDTH, CARDHEIGHT))
FOUR = pygame.image.load('Assets/4Club.png')
FOUR = pygame.transform.scale(FOUR, (CARDWIDTH, CARDHEIGHT))
FIVE = pygame.image.load('Assets/5Diamond.png')
FIVE = pygame.transform.scale(FIVE, (CARDWIDTH, CARDHEIGHT))
SIX = pygame.image.load('Assets/6Spade.png')
SIX = pygame.transform.scale(SIX, (CARDWIDTH, CARDHEIGHT))
SEVEN = pygame.image.load('Assets/7Heart.png')
SEVEN = pygame.transform.scale(SEVEN, (CARDWIDTH, CARDHEIGHT))
EIGHT = pygame.image.load('Assets/8Club.png')
EIGHT = pygame.transform.scale(EIGHT, (CARDWIDTH, CARDHEIGHT))
# CARD_WIDTH = 200
# CARD_HEIGHT = 250

CARDS = [ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT] * 2


""" Tile class """
class Tile:
    # constructor
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc

    # getter
    def getNumber(self):
        return self.number

    # check whether tile is exposed
    def isExposed(self):
        return self.exposed

    # expose the tile
    def exposeTile(self):
        self.exposed = True

    # hide the tile
    def hideTile(self):
        self.exposed = False

    # tile string method
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)

    # draw method for tiles
    def drawTile(self, canvas):
        if self.exposed:
            canvas.blit(self.number, (self.location))
        else:
            canvas.blit(CARD_BACK, (self.location))

    # selection method for tiles
    def isSelected(self, pos):
        horizontalBounds = self.location[0] <= pos[0] + 75 <= self.location[0] + CARDWIDTH
        verticalBounds = self.location[1] <= pos[1] <= self.location[1] + CARDHEIGHT
        return horizontalBounds and verticalBounds


""" helper function to initialize globals """
def new_game():
    # Initial condition of new game
    global state, turns, myTiles, exposed
    
    state = 0
    turns = 0
    random.shuffle(CARDS)
    myTiles = [Tile(CARDS[i], False, [(CARDWIDTH * i) + 75, 0]) for i in range(len(CARDS))]
    exposed = 0


"""" define button """
def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 25)
    text_render = font.render(text, True, (255,255,255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x+w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y-2), (x, y+h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y+h), (x+w, y+h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x+w, y+h), (x+w, y), 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))

""" define event handlers """
def mouseclick(pos):
    # add game state logic here
    global state, turns, turn1Tile, turn2Tile, clickedTile, exposed

    # if game has not ended, run code
    if exposed < 16:

        # check for which tile is clicked
        for tile in myTiles:
            if tile.isSelected(pos):
                clickedTile = tile

        # if clicked tile is already exposed do nothing else expose tile
        if clickedTile.isExposed():
            return
        clickedTile.exposeTile()

        # add state code here:
        if state == 0:
            state = 1
            turns += 1
            turn1Tile = clickedTile
            exposed += 1
        elif state == 1:
            state = 2
            turn2Tile = clickedTile
            exposed += 1
        elif state == 2:
            state =1
            turns += 1
            exposed += 1

            # if paired tiles don't match hide again
            if turn1Tile.getNumber() != turn2Tile.getNumber():
                turn1Tile.hideTile()
                turn2Tile.hideTile()
                exposed -= 2

            turn1Tile = clickedTile

            
""" Draw handler"""
""" cards are logically 75x100 pixels in size """
def draw(canvas):

    canvas.fill((0,0,0))

    for card in myTiles:
        card.drawTile(canvas)

    # Messages at game end
    if exposed >= 16:
        # Hide tiles
        for tile in myTiles:
            tile.hideTile()

        # Congratulatory message
        font1 = pygame.font.SysFont("Times New Roman", 60)
        label1 = font1.render("CONGRATULATIONS!", True, WHITE)
        canvas.blit(label1, (350, -5))

        # Instructions after game end
        font2 = pygame.font.SysFont("Times New Roman", 30)
        label2 = font2.render("Press restart to play another game.", True, YELLOW)
        canvas.blit(label2, (450, 55))


def main():
    # create frame and add a button and labels
    window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption("Memory")

    # get things rolling
    new_game()

    while True:

        draw(window)

        # create button
        restartButton = button(window, (5, HEIGHT / 10), "Restart")

        # draw turns label
        scoreFont = pygame.font.SysFont("Comic Sans MS", 16)
        scoreLabel = scoreFont.render("Turns: " + str(turns), True, WHITE)
        window.blit(scoreLabel, (5, 60))

        # mouseclick event listener
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(75,(75*17),75):
                    if CARD_BACK.get_rect(topleft=(i, 0)).collidepoint(x, y):
                        mouseclick((x - 75, y))
                if restartButton.collidepoint(x, y):
                    new_game()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()


# Always remember to review the grading rubric