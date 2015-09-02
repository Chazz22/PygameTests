__author__ = 'jono'

import pygame

display_size = 300
fps = 30

ball = display_size // 30
bar_height = display_size // 2

white = (255, 255, 255)
black = (0, 0, 0)


class Main:

    def __init__(self):

        self.game_exit = False
        self.game_over = False

        self.clock = None
        self.font = None
        self.game_display = None

        self.player1_pos_x = ball * 2
        self.player1_pos_y = display_size // 4

        self.player2_pos_x = display_size - (ball * 3)
        self.player2_pos_y = display_size // 4

        self.player1_ychange = 0
        self.player2_ychange = 0

        self.game_loop()

    def draw_players(self):
        pygame.draw.rect(self.game_display, black, [self.player1_pos_x, self.player1_pos_y, ball, bar_height])
        pygame.draw.rect(self.game_display, black, [self.player2_pos_x, self.player2_pos_y, ball, bar_height])

    def game_loop(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode((display_size, display_size))
        pygame.display.set_caption('Pong')

        while not self.game_exit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.player2_ychange != 0:
                            self.player2_ychange = 0
                        self.player2_ychange += ball
                    if event.key == pygame.K_UP:
                        if self.player2_ychange != 0:
                            self.player2_ychange = 0
                        self.player2_ychange += -ball

            if self.player2_pos_y < 0 or self.player2_pos_y > (display_size - bar_height):
                self.player2_ychange = 0

            self.player1_pos_y += self.player1_ychange
            self.player2_pos_y += self.player2_ychange

            self.game_display.fill(white)
            self.draw_players()

            pygame.display.update()
            self.clock.tick(fps)

Main()