__author__ = 'jono'

# Imports
import pygame, random, math

# Colors
colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0), 'green': (0, 255, 255), 'blue': (0, 0, 255), 'grey': (128, 128, 128)}
bg_color = colors['white']
splash_color = colors['black']

fps_limit = 30
display_width = 800
display_height = 600

# Gravity - points downwards with length 0.002 - arbitrary number because using pixels
gravity = (math.pi, -1)
drag = 0.99
elasticity = 0.75

caption = 'Physics Simulation'

class particle():

    def __init__(self, color, (x, y), size, game_display):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.game_display = game_display
        self.thickness = 0
        self.speed = 1
        self.angle = math.pi / 2

    def display(self):
        pygame.draw.circle(self.game_display, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        # Add to the position, in this case - a random angle and velocity
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

        # Add the gravity vector
        (self.angle, self.speed) = self.add_vectors((self.angle, self.speed), gravity)

        # Add drag
        self.speed *= drag

    # Adds two vectors to calculate the gravity vector (left in pixels)
    def add_vectors(self, (angle1, length1), (angle2, length2)):
        # Add the two vectors - one x component and one y component
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2

        # New vector length is equal to the hypotenuse of the triangle
        length = math.hypot(x, y)
        # arctan2() takes into account the '0' case
        angle = math.pi/2 - math.atan2(y, x)
        # Returns a single vector
        return (angle, length)


    def check_collision(self):

        # Particle is too far right
        if self.x > display_width - self.size:
            self.x = 2*(display_width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= elasticity
        # Particle is too far left
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        # Particle is too far down
        if self.y > display_height - self.size:
            self.y = 2*(display_height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        # Particle is too high
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


class main():

    def __init__(self):

        pygame.init()
        pygame.font.init()

        self.font = pygame.font.Font(None, 25)
        self.game_display = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(caption)

        self.particles = []

        self.game_loop()

    def game_loop(self):

        game_exit = False
        game_over = False
        game_started = False

        while not game_exit:
            # First clear the screen
            self.game_display.fill(bg_color)

            # Execute the game loop
            while not game_started:
                if self.handle_splash():
                    game_started = True

            # Pass to event handler
            self.handle_events()

            # Update particles, move and display
            for particle in self.particles:
                particle.move()
                particle.check_collision()
                particle.display()

            # Update screen
            pygame.display.update()

            # Limit FPS
            dt = self.clock.tick(fps_limit) * 1e-3

    def random_color(self):
        color = random.choice(colors.values())
        while color == bg_color or color == splash_color:
            color = random.choice(colors.values())
        return color

    def send_centered_message(self, msg, color):
        text = self.font.render(msg, True, color)
        self.game_display.blit(text, [(display_width / 2) - (text.get_rect().width / 2),
                                (display_height / 2) - (text.get_rect().height / 2)])

    def send_message(self, msg, color, xy):
        text = self.font.render(msg, True, color)
        self.game_display.blit(text, xy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                particle = self.create_particle()

                # RANDOM MOVEMENT
                particle.speed = random.randint(1, 10)
                particle.angle = random.uniform(0, math.pi * 2)

                self.particles.append(particle)

    def create_particle(self):
        return particle(self.random_color(), (random.randint(0, display_width), random.randint(0, display_height)), 10,self.game_display)

    def handle_splash(self):
        self.game_display.fill(splash_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True
        self.send_centered_message('Click the screen to begin!', bg_color)
        pygame.display.update()

main()