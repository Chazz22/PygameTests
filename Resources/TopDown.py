__author__ = 'jono'

player_radius = 10
display_height = 600
display_width = 800

import pygame

class Entity(object):

    def __init__(self, color, hp):
        # My b
        self.color = color
        self.hp = hp

    def alive(self):
        return self.hp > 0

    def draw(self):
        


class Main:

    def __init__(self):



    def game_loop(self):

