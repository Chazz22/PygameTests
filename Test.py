import turtle, random, sys

class Main:
  
  def __init__(self):
    
    sys.setExecutionLimit(1000000)
    
    self.amt_turtles = None
    self.turtles = []
    self.draw_turtle = turtle.Turtle()
    self.screen = self.draw_turtle.getscreen()
    
    self.colors = ('black', 'red', 'green', 'blue',
                  'purple', 'gray', 'pink', 'brown')
    
    self.main_loop()
    
    
  def prompt(self):
    try:
      self.amt_turtles = int(input('Amount of turtles: '))
      self.amt_turtles = self.amt_turtles - (self.amt_turtles % 4)
      print('Using {} turtles for equal spacing'.format(str(self.amt_turtles)))
    except Exception as e:
      self.prompt()
    
  def main_loop(self):
    
    self.prompt()
    
    for i in range(0, self.amt_turtles):
      turt = turtle.Turtle()
      turt.ht()
      turt.color(random.choice(self.colors))
      turt.speed(0)
      self.turtles.append(turt)
      
    self.draw_quadrants()
    
    increment = 360 / self.amt_turtles
    
    # Cannot exceed more that 10 seconds 
    for i, turt in enumerate(self.turtles):
      turt.left((i + 1) * increment)
      turt.forward(self.screen.window_width() * 1.5)
    
  def draw_quadrants(self):
    
    self.draw_turtle.reset()
    self.draw_turtle.speed(0)
    self.draw_turtle.ht()
    self.draw_turtle.pensize(4)
    self.draw_turtle.down()
    self.draw_turtle.goto(0, self.screen.window_height() / 2)
    self.draw_turtle.goto(0, 0)
    self.draw_turtle.goto(-self.screen.window_width() / 2, 0)
    self.draw_turtle.goto(0, 0)
    self.draw_turtle.goto(self.screen.window_width() / 2, 0)
    self.draw_turtle.goto(0, 0)
    self.draw_turtle.goto(0, -self.screen.window_height() / 2)
    self.draw_turtle.pensize(1)

  
Main()

