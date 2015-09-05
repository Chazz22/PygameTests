__author__ = 'jono'

import pygame, math, random, time
from abc import abstractmethod, ABCMeta

display_size = 500
fps = 30

ball_size = display_size // 30
paddle_height = display_size // 3
paddle_speed = ball_size // 1.2
ball_speed = ball_size * 1.1
button_width = int(display_size * .15)
button_height = int(button_width * 0.6)

white = (255, 255, 255)
grey = (128, 128, 128)
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

    @abstractmethod
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
    is_bot = False

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
        ball_range = [random.uniform(-math.pi / 10, math.pi / 10), random.uniform(3 * math.pi / 4, 5 * math.pi / 4)]
        self.x = self.origin_x
        self.y = self.origin_y
        self.angle = random.choice(ball_range)


class BaseMenu(object):

    def __init__(self, main, buttons, enabled=False):
        self.main = main
        self.buttons = buttons
        self.enabled = enabled

    def draw(self):
        if not self.enabled:
            return
        for button in self.buttons:
            button.draw()

    def check_hover(self):
        if not self.enabled:
            return
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        for button in self.buttons:
            if button.x < mouse_x < button.x + button_width and button.y < mouse_y < button.y + button_height:
                button.is_highlighted = True
            else:
                button.is_highlighted = False

    def check_click(self):
        if not self.enabled:
            return
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        for button in self.buttons:
            if button.x < mouse_x < button.x + button_width and button.y < mouse_y < button.y + button_height:
                return button.click()


class MainMenu(BaseMenu):

    def __init__(self, main):
        self.main = main
        self.buttons = ([Button(self.main, 'Play', display_size // 2 - button_width / 2, display_size // 2 - button_height)])
        BaseMenu.__init__(self, main, self.buttons)


class PlayerSelectionMenu(BaseMenu):

    def __init__(self, main):
        self.main = main
        self.buttons = ([Button(self.main, '1 Player', display_size // 2 - button_width / 2, display_size // 3)
                         , Button(self.main, '2 Player', display_size // 2 - button_width / 2, (display_size // 3) + button_height * 1.2)
                         , Button(self.main, '0 Player', display_size // 2 - button_width / 2, (display_size // 3) + 2 * button_height * 1.2)])
        BaseMenu.__init__(self, main, self.buttons)


class Button(object):

    def __init__(self, main, name, x, y):
        self.main = main
        self.game_display = main.game_display
        self.font = main.hud.font
        self.is_highlighted = False
        self.name = name
        self.x = x
        self.y = y

    def draw(self):

        if self.is_highlighted:
            pygame.draw.rect(self.game_display, grey, (self.x, self.y, button_width, button_height))
        else:
            pygame.draw.rect(self.game_display, black, (self.x, self.y, button_width, button_height))
        text = self.font.render(self.name, True, white)
        self.game_display.blit(text, (self.x, self.y))

    def click(self):
        return self.name


class Hud(object):

    def __init__(self, main):
        self.main = main
        self.game_display = main.game_display
        self.font = main.font

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
        pygame.font.init()
        self.font = pygame.font.Font(None, display_size // 20)
        self.game_display = pygame.display.set_mode((display_size, display_size))
        pygame.display.set_caption('Pong')
        pygame.mixer.init()
        self.pongblip = pygame.mixer.Sound('Resources/pongblip.wav')
        self.pongblip2 = pygame.mixer.Sound('Resources/pongblip2.wav')

        self.player1 = None
        self.player2 = None
        self.ball = None

        self.hud = Hud(self)
        self.main_menu = MainMenu(self)
        self.player_selection_menu = PlayerSelectionMenu(self)

        self.game_loop()

    def reset(self):
        self.player1.reset()
        self.player2.reset()
        self.ball.reset()

    def game_loop(self):

        self.main_menu.enabled = True

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu.check_click() == 'Play':
                        self.main_menu.enabled = False
                        self.player_selection_menu.enabled = True

            self.game_display.fill(white)
            if self.player_selection_menu.enabled:
                self.player_selection_menu.check_hover()
                self.player_selection_menu.draw()
            if self.main_menu.enabled:
                self.main_menu.check_hover()
                self.main_menu.draw()
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
                self.pongblip2.play()
                time.sleep(0.5)
            elif self.ball.x > display_size - ball_size:
                self.reset()
                self.player1.score += 1
                self.pongblip2.play()
                time.sleep(0.5)
            if self.ball.y < ball_size:
                self.ball.angle = -self.ball.angle
                self.ball.y = 2 * ball_size - self.ball.y
                self.pongblip2.play()
            elif self.ball.y > display_size - ball_size:
                self.ball.angle = -self.ball.angle
                self.ball.y = 2 * (display_size - ball_size) - self.ball.y
                self.pongblip2.play()

            # Ball collision with paddles
            # For x coords, must use math.pi - angle to shift for cos
            if self.player1.x < self.ball.x < self.player1.x + ball_size and self.player1.y < self.ball.y < self.player1.y + paddle_height:
                self.ball.angle = math.pi - self.ball.angle - (self.player1.angle / 10)
                self.ball.x = 2 * (self.player1.x + ball_size) - self.ball.x
                self.pongblip.play()
            if self.player2.x < self.ball.x < self.player2.x + ball_size and self.player2.y < self.ball.y < self.player2.y + paddle_height:
                self.ball.angle = math.pi - self.ball.angle - (self.player2.angle / 10)
                self.ball.x = 2 * self.player2.x - self.ball.x
                self.pongblip.play()

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