__author__ = 'jono'

import pygame, random, math

pygame.init()
pygame.font.init()

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

clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

def snake(snakelist):
    for xy in snakelist:
        pygame.draw.rect(gameDisplay, RED, [xy[0], xy[1], block_size, block_size])


def sendMessage(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [(display_width / 2) - (screen_text.get_rect().width / 2), display_height / 2])

def dist(x1, x2, y1, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def gameLoop():

    gameExit = False
    gameOver = False

    pos_x = display_width / 2
    pos_y = display_height / 2
    pos_x_change = 0
    pos_y_change = 0

    apple_x = round(random.randrange(0, display_width - block_size) / block_size) * block_size
    apple_y = round(random.randrange(0, display_height - block_size) / block_size) * block_size

    snakeList = []
    snakeLength = 1

    while not gameExit:

        while gameOver:
            gameDisplay.fill(WHITE)
            sendMessage("Game over, click the screen to play again!", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gameLoop()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pos_x_change = -block_size
                    pos_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    pos_x_change = block_size
                    pos_y_change = 0
                elif event.key == pygame.K_UP:
                    pos_y_change = -block_size
                    pos_x_change = 0
                elif event.key == pygame.K_DOWN:
                    pos_y_change = block_size
                    pos_x_change = 0

        if SNAKE_BOT:
            if pos_x < apple_x:

                pos_x_change = block_size
                pos_y_change = 0

            if pos_x > apple_x:
                pos_x_change = -block_size
                pos_y_change = 0
            if pos_y < apple_y:
                pos_y_change = block_size
                pos_x_change = 0
            if pos_y > apple_y:
                pos_y_change = -block_size
                pos_x_change = 0

        # Game barrier
        if pos_x > display_width or pos_x < 0 or pos_y > display_height or pos_y < 0:
            gameOver = True

        pos_x += pos_x_change
        pos_y += pos_y_change

        gameDisplay.fill(WHITE)
        pygame.draw.rect(gameDisplay, GREEN, [apple_x, apple_y, block_size, block_size])
        pygame.draw.rect(gameDisplay, RED, [pos_x, pos_y, block_size, block_size])

        if pos_x == apple_x and pos_y == apple_y:
            snakeLength += 1
            apple_x = round(random.randrange(0, display_width - block_size) / 10) * 10
            apple_y = round(random.randrange(0, display_height - block_size) / 10) * 10

        snakeHead = []
        snakeHead.append(pos_x)
        snakeHead.append(pos_y)
        snakeList.append(snakeHead)

        if (len(snakeList) > snakeLength):
            del snakeList[0]

        for snakepart in snakeList[:-1]:
            if snakepart == snakeHead:
                gameOver = True

        snake(snakeList)

        pygame.display.update()
        clock.tick(fps)

gameLoop()

pygame.quit()
quit()