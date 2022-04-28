from pygame import Color


class Brush:
    def __init__(self, color=Color(0,0,0), radius=5):
        self.color = color
        self.radius = radius
