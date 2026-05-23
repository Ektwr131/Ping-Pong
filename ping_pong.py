from pygame import *

init()

window = display.set_mode((700, 500))
display.set_caption('Ping Pong')

game = True

background_color = (0, 250, 250)

FPS = 60
game_clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(background_color)

    game_clock.tick(FPS)
    display.update()