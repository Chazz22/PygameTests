__author__ = 'jono'

import pygame, math
from abc import abstractmethod

display_size = 500
fps = 30

ball = display_size // 30
bar_height = display_size // 3

white = (255, 255, 255)
black = (0, 0, 0)


class Entity:

    def __init__(self, game_display, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.game_display = game_display

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    @abstractmethod
    def draw(self):
        pass

class Paddle(Entity):




class Ball(Entity):

    def __init__(self, radius):
        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.game_display, )

class Main:

    def __init__(self):

        self.game_exit = False
        self.game_over = False

        self.game_started = False

        self.clock = None
        self.font = None
        self.game_display = None

        self.player1_pos_x = ball * 2
        self.player1_pos_y = display_size // 4

        self.player2_pos_x = display_size - (ball * 3)
        self.player2_pos_y = display_size // 4

        self.player1_ychange = 0
        self.player2_ychange = 0

        self.player1_score = 0
        self.player2_score = 0

        self.game_loop()

    def draw_players(self):
        pygame.draw.rect(self.game_display, black, [self.player1_pos_x, self.player1_pos_y, ball, bar_height])
        pygame.draw.rect(self.game_display, black, [self.player2_pos_x, self.player2_pos_y, ball, bar_height])

    def scoreboard(self):
        text = self.font.render('{}:{}'.format(self.player1_score, self.player2_score), True, black)
        self.game_display.blit(text, ((display_size // 2) - (text.get_rect().width // 2), ball))

    def send_centered_message(self, msg):
        text = self.font.render(msg, True, black)
        self.game_display.blit(text, ((display_size // 2) - (text.get_rect().width // 2), display_size // 2))

    def game_loop(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, display_size // 10)
        self.game_display = pygame.display.set_mode((display_size, display_size))
        pygame.display.set_caption('Pong')

        while not self.game_started:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.game_started = True

            self.game_display.fill(white)
            self.send_centered_message('Press any key to begin!')

            pygame.display.update()

        while not self.game_exit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player2_ychange = 0
                        self.player2_ychange += ball
                    elif event.key == pygame.K_UP:
                        self.player2_ychange = 0
                        self.player2_ychange += -ball
                    elif event.key == pygame.K_w:
                        self.player1_ychange = 0
                        self.player1_ychange += -ball
                    elif event.key == pygame.K_s:
                        self.player1_ychange = 0
                        self.player1_ychange += ball

            if self.player2_pos_y < 0:
                self.player2_pos_y = 0
            elif self.player2_pos_y > (display_size - bar_height):
                self.player2_pos_y = display_size - bar_height

            if self.player1_pos_y < 0:
                self.player1_pos_y = 0
            elif self.player1_pos_y > (display_size - bar_height):
                self.player1_pos_y = display_size - bar_height

            self.player1_pos_y += self.player1_ychange
            self.player2_pos_y += self.player2_ychange

            self.game_display.fill(white)
            self.draw_players()
            self.scoreboard()

            pygame.display.update()
            self.clock.tick(fps)

Main()