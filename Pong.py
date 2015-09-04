__author__ = 'jono'

import pygame, math, random
from abc import abstractmethod, ABCMeta

display_size = 500
fps = 30

ball_size = display_size // 30
paddle_height = display_size // 3

white = (255, 255, 255)
black = (0, 0, 0)


class BaseEntity(object):

    __metaclass__ = ABCMeta

    def __init__(self, game_display, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.game_display = game_display

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Paddle(BaseEntity):

    score = 0

    def draw(self):
        pygame.draw.rect(self.game_display, black, [self.x, self.y, ball_size, paddle_height])

    def move(self):
        self.y += int(math.sin(self.angle) * self.speed)


class Ball(BaseEntity):

    radius = ball_size // 2

    def draw(self):
        pygame.draw.circle(self.game_display, black, (self.x, self.y), self.radius, 0)

    def move(self):
        self.x += int(math.sin(self.angle) * self.speed)
        self.y -= int(math.cos(self.angle) * self.speed)

    def reset(self):
        self.x = display_size // 2
        self.y = display_size // 2
        self.angle = random.uniform(-math.pi / 4, math.pi / 4)


class Main:

    def __init__(self):

        self.game_exit = False
        self.game_over = False

        self.game_started = False

        self.clock = None
        self.font = None
        self.game_display = None

        self.player1 = None
        self.player2 = None
        self.ball = None

        self.game_loop()

    def scoreboard(self):
        text = self.font.render('{}:{}'.format(self.player1.score, self.player2.score), True, black)
        self.game_display.blit(text, ((display_size // 2) - (text.get_rect().width // 2), ball_size))

    def send_centered_message(self, msg):
        text = self.font.render(msg, True, black)
        self.game_display.blit(text, ((display_size // 2) - (text.get_rect().width // 2), display_size // 2))

    def game_loop(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, display_size // 10)
        self.game_display = pygame.display.set_mode((display_size, display_size))
        pygame.display.set_caption('Pong')

        self.player1 = Paddle(self.game_display, ball_size * 2, display_size // 4, 0, ball_size)
        self.player2 = Paddle(self.game_display, display_size - (ball_size * 3), display_size // 4, 0, ball_size)

        self.ball = Ball(self.game_display, display_size // 2, display_size // 2
                         , random.uniform(-2 * math.pi, 2 * math.pi), ball_size // 1.2)

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

            # Draw bg first
            self.game_display.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player2.angle = math.pi / 2
                    elif event.key == pygame.K_UP:
                        self.player2.angle = -math.pi / 2
                    elif event.key == pygame.K_w:
                        self.player1.angle = -math.pi / 2
                    elif event.key == pygame.K_s:
                        self.player1.angle = math.pi / 2

            # Paddle collision with y bounds
            if self.player2.y < 0:
                self.player2.y = 0
            elif self.player2.y > (display_size - paddle_height):
                self.player2.y = display_size - paddle_height

            if self.player1.y < 0:
                self.player1.y = 0
            elif self.player1.y > (display_size - paddle_height):
                self.player1.y = display_size - paddle_height

            # Ball collision with wall bounds
            if self.ball.x < ball_size:
                self.ball.reset()
                self.player2.score += 1
            elif self.ball.x > display_size - ball_size:
                self.ball.reset()
                self.player1.score += 1
            if self.ball.y < ball_size:
                # For y coords, must use math.pi - angle to shift for cos
                self.ball.angle = math.pi - self.ball.angle
                self.ball.y = 2 * ball_size - self.ball.y
            elif self.ball.y > display_size - ball_size:
                self.ball.angle = math.pi - self.ball.angle
                self.ball.y = 2 * (display_size - ball_size) - self.ball.y

            # Ball collision with paddles
            if self.player1.x < self.ball.x < self.player1.x + ball_size and self.player1.y < self.ball.y < self.player1.y + paddle_height:
                self.ball.angle = -self.ball.angle
                self.ball.x = 2 * (self.player1.x + ball_size) - self.ball.x
            if self.player2.x < self.ball.x < self.player2.x + ball_size and self.player2.y < self.ball.y < self.player2.y + paddle_height:
                self.ball.angle = -self.ball.angle
                self.ball.x = 2 * self.player2.x - self.ball.x

            self.player1.move()
            self.player2.move()
            self.ball.move()

            # Update screen
            self.player1.draw()
            self.player2.draw()
            self.ball.draw()
            self.scoreboard()

            pygame.display.update()
            self.clock.tick(fps)

Main()