__author__ = 'jono'

# Imports
import pygame, random, math

# Colors
colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0), 'green': (0, 255, 255), 'blue': (0, 0, 255), 'grey': (128, 128, 128)}
bg_color = colors['white']
splash_color = colors['black']

caption = 'Agar.io Clone'

fps_limit = 100
display_width = 800
display_height = 600

class player_cell():

    def __init__(self, game_display, color, (x, y)):
        self.game_display = game_display
        # For now, generates a random color
        self.color = color
        self.x = x
        self.y = y
        # Starting size of a player cell
        self.size = 20
        # Speed
        self.speed = 0.10

    def display(self):
        pygame.draw.circle(self.game_display, self.color, (int(self.x), int(self.y)), self.size)

    # Will make the player cell move toward desired pos
    def move(self, (x, y), dt):

        if (self.x < x):
            self.x += self.speed * dt
        elif (self.x > x):
            self.x -= self.speed * dt

        if (self.y > y):
            self.y -= self.speed * dt
        elif(self.y < y):
            self.y += self.speed * dt

    def grow(self):
        self.size += 1

class cell():

    def __init__(self, game_display, color, (x, y)):
        self.game_display = game_display
        self.x = x
        self.y = y
        self.color = color
        self.size = 5

    def display(self):
        pygame.draw.circle(self.game_display, self.color, (self.x, self.y), self.size)

class main():
    def __init__(self):

        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(caption)

        self.game_display = pygame.display.set_mode((display_width, display_height))
        self.font = pygame.font.Font(None, 25)
        self.clock = pygame.time.Clock()

        self.game_loop()

    def game_loop(self):

        game_exit = False
        game_started = False

        cells = []
        max_cells = 200

        while len(cells) < max_cells:
            cells.append(cell(self.game_display, self.random_color(), (random.randrange(0, display_width), random.randrange(0, display_height))))

        player = self.create_player()

        while not game_exit:

            dt = self.clock.tick(fps_limit)

            # Set bg color
            self.game_display.fill(bg_color)

            while not game_started:
                if self.handle_splash():
                    game_started = True

            self.handle_events()

            for c in cells:

                # Check collision
                dist = int(math.sqrt((c.x - player.x)**2 + (c.y - player.y)**2))
                if dist < player.size + c.size:
                    del(cells[cells.index(c)])
                    player.grow()

                c.display()

            player.move(pygame.mouse.get_pos(), dt)
            player.display()

            pygame.display.update()

    def handle_splash(self):

        # Set splash bg
        self.game_display.fill(splash_color)
        self.send_centered_message('Click to start playing!', bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

        dt = self.clock.tick(fps_limit)
        pygame.display.update()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def create_player(self):
        return player_cell(self.game_display, self.random_color(), (display_width / 2, display_height / 2))

    def send_centered_message(self, msg, color):
        text = self.font.render(msg, True, color)
        self.game_display.blit(text, [(display_width / 2) - (text.get_rect().width / 2),
                                (display_height / 2) - (text.get_rect().height / 2)])

    def send_message(self, msg, color, xy):
        text = self.font.render(msg, True, color)
        self.game_display.blit(text, xy)

    def random_color(self):
        color = random.choice(colors.values())
        while color == bg_color or color == splash_color:
            color = random.choice(colors.values())
        return color


main()