from pygame import *

init()

window = display.set_mode((700, 500))
display.set_caption("Ping Pong")

background_color = (0, 250, 250)

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


class Ball(GameSprite):

    def __init__(self, x, y, speed_x, speed_y):
        super().__init__(x, y, 40, 40, 0, (255, 255, 255))

        self.image = transform.scale(
            image.load("ball.png"),
            (80, 60)
        )

        self.rect = self.image.get_rect(center=(x, y))

        self.speed_x = speed_x
        self.speed_y = speed_y

    def action(self):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y <= 0:
            self.speed_y *= -1

        if self.rect.y >= 500 - self.rect.height:
            self.speed_y *= -1


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


left_bar = LeftBar(20, 190, 20, 120, 5, (0, 255, 0))
right_bar = RightBar(660, 190, 20, 120, 5, (255, 0, 0))

ball = Ball(340, 240, 4, 4)

game = True

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(background_color)

    left_bar.action()
    right_bar.action()
    ball.action()

    if sprite.collide_rect(ball, left_bar):
        ball.speed_x *= -1

    if sprite.collide_rect(ball, right_bar):
        ball.speed_x *= -1

    if ball.rect.x <= 0:
        ball.speed_x *= -1

    if ball.rect.x >= 700 - ball.rect.width:
        ball.speed_x *= -1

    left_bar.reset()
    right_bar.reset()
    ball.reset()

    display.update()
    game_clock.tick(FPS)
