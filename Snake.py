__author__ = 'jono'

import pygame, random, math

display_width = 300
display_height = 300

fps = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SNAKE_BOT = True

block_size = 10

class Main:


    def __init__(self):

        self.gameExit = False
        self.gameOver = False

        self.pos_x = display_width / 2
        self.pos_y = display_height / 2
        self.pos_x_change = 0
        self.pos_y_change = 0

        self.apple_x = round(random.randrange(0, display_height - block_size) / block_size) * block_size
        self.apple_y = round(random.randrange(0, display_height - block_size) / block_size) * block_size

        self.snakeList = []
        self.snakeLength = 1

        self.font = None
        self.clock = None

        self.gameLoop()

    def snake(self, snakelist):
        for xy in snakelist:
            pygame.draw.rect(self.gameDisplay, RED, [xy[0], xy[1], block_size, block_size])

    def sendMessage(self, msg, color):
        screen_text = self.font.render(msg, True, color)
        self.gameDisplay.blit(screen_text, [(display_width / 2) - (screen_text.get_rect().width / 2), display_height / 2])

    def scan_vertical(self):
        for part in self.snakeList[:-1]:
            if part[1] == self.pos_y:
                if part[1] > self.pos_y:
                    

    def gameLoop(self):

        pygame.init()
        pygame.font.init()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)

        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Snake")

        while not self.gameExit:

            while self.gameOver:
                self.gameDisplay.fill(WHITE)
                self.sendMessage("Game over, click the screen to play again!", RED)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.gameLoop()

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pos_x_change = -block_size
                        self.pos_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.pos_x_change = block_size
                        self.pos_y_change = 0
                    elif event.key == pygame.K_UP:
                        self.pos_y_change = -block_size
                        self.pos_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.pos_y_change = block_size
                        self.pos_x_change = 0

            if SNAKE_BOT:

                # Left of the apple
                if self.pos_x < self.apple_x:

                # Right of the apple
                elif self.pos_x > self.apple_x:

                # Under apple
                elif self.pos_y < self.apple_y:

                # Above apple
                elif self.pos_y > self.apple_y:

            # Game barrier
            if self.pos_x > display_width or self.pos_x < 0 or self.pos_y > display_height or self.pos_y < 0:
                self.gameOver = True

            self.pos_x += self.pos_x_change
            self.pos_y += self.pos_y_change

            self.gameDisplay.fill(WHITE)
            pygame.draw.rect(self.gameDisplay, GREEN, [self.apple_x, self.apple_y, block_size, block_size])
            pygame.draw.rect(self.gameDisplay, RED, [self.pos_x, self.pos_y, block_size, block_size])

            if self.pos_x == self.apple_x and self.pos_y == self.apple_y:
                self.snakeLength += 1
                self.apple_x = round(random.randrange(0, display_width - block_size) / 10) * 10
                self.apple_y = round(random.randrange(0, display_height - block_size) / 10) * 10

            snakeHead = []
            snakeHead.append(self.pos_x)
            snakeHead.append(self.pos_y)
            self.snakeList.append(snakeHead)

            if len(self.snakeList) > self.snakeLength:
                del self.snakeList[0]

            for snakepart in self.snakeList[:-1]:
                if snakepart == snakeHead:
                    self.gameOver = True

            self.snake(self.snakeList)

            pygame.display.update()
            self.clock.tick(fps)

Main()