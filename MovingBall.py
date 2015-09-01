__author__ = 'jono'

import pygame
from pygame import gfxdraw
import random
import math

pygame.init()
pygame.font.init()

# Declare variables

colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 255), "blue": (0, 0, 255)}

tickrate = 60

display_width = 800
display_height = 600

cellSize = 10

font = pygame.font.Font(None, 25)
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption("Agar.io Clone")

class main():

    def __init__(self):
        self.gameLoop()

    def sendCenteredMessage(self, msg, color):
        text = font.render(msg, True, color)
        gameDisplay.blit(text, [(display_width / 2) - (text.get_rect().width / 2),
                                (display_height / 2) - (text.get_rect().height / 2)])

    def sendMessage(self, msg, color, xy):
        text = font.render(msg, True, color)
        gameDisplay.blit(text, [xy[0], xy[1]])

    def euclideanDist(self, x1, y1, x2, y2):
        return math.sqrt(((x1-x2)**2) + ((y1-y2))**2)

    def drawPlayer(self, xy, playerColor, playerSize):
        # pygame.draw.circle(gameDisplay, playerColor, xy, playerSize)
        rect1 = pygame.gfxdraw.filled_circle(gameDisplay, xy[0], xy[1], playerSize, playerColor)
        rect2 = pygame.gfxdraw.aacircle(gameDisplay, xy[0], xy[1], playerSize, playerColor)

    def grow(self, playerSize):
        return playerSize + 1

    def drawCell(self, cellColor, cellSize):
        return pygame.draw.circle(gameDisplay, cellColor, (random.randrange(10, 790), random.randrange(10, 590)), cellSize)

    def handleMotion(self, playerPos, mouse, speed):

        playerPosChange = [0, 0]

        playerX = playerPos[0]
        playerY = playerPos[1]

        mouseX = mouse.get_pos()[0]
        mouseY = mouse.get_pos()[1]

        # Handle speed vector
        if self.euclideanDist(playerX, playerY, mouseX, mouseY) < 10:
            speed = 0
        elif self.euclideanDist(playerX, playerY, mouseX, mouseY) < 50:
            speed = speed / 2


        # Handle direction vector
        if mouseX < playerX:
            playerPosChange[0] = -speed
        else:
            playerPosChange[0] = speed

        if mouseY < playerY:
            playerPosChange[1] = -speed
        else:
            playerPosChange[1] = speed

        return playerPosChange


    def gameLoop(self):

        # Declare variables

        gameExit = False
        gameOver = False
        gameStarted = False

        playerPos = [display_width / 2, display_height / 2]
        playerPosChange = [0, 0]

        playerSize = 30
        playerSpeed = 5 # constant for now

        playerColor = random.choice(colors.values())

        cells = []
        cellAmt = 10
        cellSize = 10
        cellColor = random.choice(colors.values())

        while(cellColor == colors["white"] or cellColor == playerColor):
            cellColor = random.choice(colors.values())

        while(playerColor == colors["white"]):
            playerColor = random.choice(colors.values())

        while not gameExit:
            gameDisplay.fill(colors["white"])

            while not gameStarted:
                gameDisplay.fill(colors["white"])
                self.sendCenteredMessage("Click to start game!", colors["black"])
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameStarted = True

            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    # playerPosChange = handleMotion(playerPos, pygame.mouse, playerSpeed)
                    playerPosChange = self.handleMotion(playerPos, pygame.mouse, playerSpeed)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Must also poll for movement when idle
            playerPosChange = self.handleMotion(playerPos, pygame.mouse, playerSpeed)

            playerPos[0] += playerPosChange[0]
            playerPos[1] += playerPosChange[1]

            # playerRect[0].move(playerPosChange[0], playerPosChange[1])
            # playerRect[1].move(playerPosChange[0], playerPosChange[1])

            # playerRect.move(playerPosChange[0], playerPosChange[1])

            self.drawPlayer(playerPos, playerColor, playerSize)

            while len(cells) < cellAmt:
                cells.append(self.drawCell(cellColor, cellSize))

            pygame.display.update()
            clock.tick(tickrate)

main()
