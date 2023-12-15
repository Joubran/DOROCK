import pygame as pg

class Slider:
    def __init__(self, x, y, w, h, screen):
        self.circle_x = x
        self.volume = 100
        self.sliderRect = pg.Rect(x, y, w, h)
        self.clicked = False
        self.circle = pg.draw.circle(screen, (0, 10, 0), (self.circle_x, (self.sliderRect.h / 2 + self.sliderRect.y)), self.sliderRect.h * 1.5)
    def draw(self, screen, vol=1):
        pg.draw.rect(screen, (250, 250, 250), self.sliderRect)
        if vol == 0:
            pg.draw.circle(screen, (250, 240, 250), (self.sliderRect.x,  self.sliderRect.y + self.sliderRect.h/2), self.sliderRect.h * 1.5)
        else:
            pg.draw.circle(screen, (250, 240, 250), (self.circle_x, (self.sliderRect.h / 2 + self.sliderRect.y)), self.sliderRect.h * 1.5)

    def get_volume(self):
        return self.volume

    def set_volume(self, num):
        self.volume = num

    def update_volume(self, x):
        if x < self.sliderRect.x:
            self.volume = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.volume = 100
        else:
            self.volume = int((x - self.sliderRect.x) / float(self.sliderRect.w) * 100)

    def on_slider(self, x, y):
        if self.on_slider_hold(x, y) or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h:
            return True
        else:
            return False

    def on_slider_hold(self, x, y):
        if self.circle.collidepoint(x, y) and pg.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
        if not pg.mouse.get_pressed()[0]:
            self.clicked = False
        return self.clicked

    def handle_event(self, screen, x):
        if x < self.sliderRect.x:
            self.circle_x = self.sliderRect.x
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.circle_x = self.sliderRect.x + self.sliderRect.w
        else:
            self.circle_x = x
        self.draw(screen)
        self.update_volume(x)