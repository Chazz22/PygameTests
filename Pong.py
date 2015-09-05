__author__ = 'jono'

import pygame, math, random, time
from abc import abstractmethod, ABCMeta

display_size = 500
fps = 30

ball_size = display_size // 30
paddle_height = display_size // 3
paddle_speed = ball_size // 1.2
ball_speed = ball_size

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
        self.origin_x = self.x
        self.origin_y = self.y
        self.origin_angle = self.angle

    def move(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
        self.angle = self.origin_angle


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
        self.x += int(math.cos(self.angle) * self.speed)
        self.y -= int(math.sin(self.angle) * self.speed)

    def reset(self):
        ball_range = [random.uniform(-math.pi / 8, math.pi / 8), random.uniform(3 * math.pi / 4, 5 * math.pi / 4)]
        self.x = display_size // 2
        self.y = display_size // 2
        self.angle = random.choice(ball_range)


class Hud(object):

    def __init__(self, main):
        self.main = main
        self.game_display = main.game_display
        pygame.font.init()
        self.font = pygame.font.Font(None, display_size // 10)

    def draw_line(self):
        pygame.draw.line(self.game_display, black, (display_size // 2, 0), (display_size // 2, display_size))

    def update_scoreboard(self):
        text = self.font.render('{}:{}'.format(self.main.player1.score, self.main.player2.score), True, black)
        self.game_display.blit(text, ((display_size // 2) - (text.get_rect().width // 2), ball_size))

    def send_centered_message(self, msg):
        text = self.font.render(msg, True, black)
        self.game_display.blit(text, ((display_size // 2) - (text.get_rect().width // 2), display_size // 2))

    def update(self):
        self.update_scoreboard()
        self.draw_line()


class Main:

    def __init__(self):

        self.game_exit = False
        self.game_over = False

        self.game_started = False

        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode((display_size, display_size))
        pygame.display.set_caption('Pong')

        self.player1 = None
        self.player2 = None
        self.ball = None

        self.hud = Hud(self)

        self.game_loop()

    def reset(self):
        self.player1.reset()
        self.player2.reset()
        self.ball.reset()

    def game_loop(self):

        self.player1 = Paddle(self.game_display, ball_size * 2, display_size // 4, 0, paddle_speed)
        self.player2 = Paddle(self.game_display, display_size - (ball_size * 3), display_size // 4, 0, paddle_speed)

        self.ball = Ball(self.game_display, display_size // 2, display_size // 2
                         , 0, ball_speed)
        self.ball.reset()

        while not self.game_started:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.game_started = True

            self.game_display.fill(white)
            self.hud.send_centered_message('Press any key to begin!')

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
                self.reset()
                self.player2.score += 1
                time.sleep(0.5)
            elif self.ball.x > display_size - ball_size:
                self.reset()
                self.player1.score += 1
                time.sleep(0.5)
            if self.ball.y < ball_size:
                self.ball.angle = -self.ball.angle
                self.ball.y = 2 * ball_size - self.ball.y
            elif self.ball.y > display_size - ball_size:
                self.ball.angle = -self.ball.angle
                self.ball.y = 2 * (display_size - ball_size) - self.ball.y

            # Ball collision with paddles
            # For x coords, must use math.pi - angle to shift for cos
            if self.player1.x < self.ball.x < self.player1.x + ball_size and self.player1.y < self.ball.y < self.player1.y + paddle_height:
                self.ball.angle = math.pi - self.ball.angle - (self.player1.angle / 6)
                self.ball.x = 2 * (self.player1.x + ball_size) - self.ball.x
            if self.player2.x < self.ball.x < self.player2.x + ball_size and self.player2.y < self.ball.y < self.player2.y + paddle_height:
                self.ball.angle = math.pi - self.ball.angle - (self.player2.angle / 6)
                self.ball.x = 2 * self.player2.x - self.ball.x

            self.player1.move()
            self.player2.move()
            self.ball.move()

            # Update screen
            self.player1.draw()
            self.player2.draw()
            self.ball.draw()
            self.hud.update()

            pygame.display.update()
            self.clock.tick(fps)

Main()