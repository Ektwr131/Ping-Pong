from pygame import *

init()

window = display.set_mode((700, 500))
display.set_caption('Ping Pong')

ball = transform.scale(image.load("ball.png"), (100, 75))

background_color = (0, 250, 250)
bar_color = (255, 255, 255)

FPS = 60
game_clock = time.Clock()

class GameSprite(sprite.Sprite):

    def __init__(self, x, y, width, height, speed, color):
        super().__init__()

        self.image = Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class LeftBar(GameSprite):

    def action(self):

        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < 500 - self.rect.height:
            self.rect.y += self.speed

class RightBar(GameSprite):

    def action(self):

        keys = key.get_pressed()

        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < 500 - self.rect.height:
            self.rect.y += self.speed

left_bar = LeftBar(20, 200, 20, 100, 7, bar_color)
right_bar = RightBar(660, 200, 20, 100, 7, bar_color)

game = True

while game:

    for e in event.get():

        if e.type == QUIT:
            game = False

    window.fill(background_color)

    window.blit(ball, (300, 230))

    left_bar.action()
    right_bar.action()

    left_bar.reset()
    right_bar.reset()

    display.update()
    game_clock.tick(FPS)