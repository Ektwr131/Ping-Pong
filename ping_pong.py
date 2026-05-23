from pygame import *

init()

window = display.set_mode((700, 500))
display.set_caption('Ping Pong')
ball = transform.scale(image.load("ball.png"), (100, 75))

game = True

background_color = (0, 250, 250)

FPS = 60
game_clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(background_color)
    window.blit(ball, (300, 230))
    
    game_clock.tick(FPS)
    display.update()