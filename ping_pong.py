import pygame

pygame.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Ping Pong")

background_color = (0, 250, 250)

FPS = 60
game_clock = pygame.time.Clock()

game_state = "menu"
mode = None
difficulty = None

bot_settings = {
    "easy": {"speed": 6, "delay": 4},
    "medium": {"speed": 8, "delay": 3},
    "hard": {"speed": 10, "delay": 2},
    "extreme": {"speed": 12, "delay": 1},
    "nightmare": {"speed": 14, "delay": 0},
}

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
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
        self.image = pygame.transform.scale(pygame.image.load("ball.png"), (80, 60))
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < 500 - self.rect.height:
            self.rect.y += self.speed

class RightBar(GameSprite):
    def action(self, ball=None):
        if mode == "bot":
            settings = bot_settings[difficulty]
            if pygame.time.get_ticks() % (settings["delay"] + 1) == 0:
                if ball.rect.centery > self.rect.centery and self.rect.y < 500 - self.rect.height:
                    self.rect.y += settings["speed"]
                if ball.rect.centery < self.rect.centery and self.rect.y > 0:
                    self.rect.y -= settings["speed"]
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.y < 500 - self.rect.height:
                self.rect.y += self.speed

left_bar = LeftBar(20, 190, 20, 120, 5, (0, 255, 0))
right_bar = RightBar(660, 190, 20, 120, 5, (255, 0, 0))
ball = Ball(340, 240, 4, 4)

pygame.font.init()
losefont = pygame.font.Font(None, 50)

lose1 = losefont.render("PLAYER 1 LOSE", True, (255, 0, 0))
lose2 = losefont.render("PLAYER 2 LOSE", True, (255, 0, 0))

def draw_menu():
    window.fill((0, 0, 0))
    title = losefont.render("PING PONG", True, (255, 255, 255))
    pvp = losefont.render("Press 1: Player vs Player", True, (0, 255, 0))
    bot = losefont.render("Press 2: Player vs Bot", True, (0, 0, 255))
    window.blit(title, (250, 100))
    window.blit(pvp, (150, 220))
    window.blit(bot, (150, 280))

def draw_difficulty():
    window.fill((20, 20, 20))
    text = losefont.render("Choose Difficulty", True, (255, 255, 255))
    window.blit(text, (200, 100))
    options = ["1: Easy", "2: Medium", "3: Hard", "4: Extreme", "5: Nightmare"]
    for i, t in enumerate(options):
        render = losefont.render(t, True, (200, 200, 0))
        window.blit(render, (180, 180 + i * 40))

game = True
game_over = False
loser_text = ""

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

        if game_state == "menu":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    mode = "pvp"
                    game_state = "playing"
                if e.key == pygame.K_2:
                    mode = "bot"
                    game_state = "difficulty"

        elif game_state == "difficulty":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    difficulty = "easy"
                elif e.key == pygame.K_2:
                    difficulty = "medium"
                elif e.key == pygame.K_3:
                    difficulty = "hard"
                elif e.key == pygame.K_4:
                    difficulty = "extreme"
                elif e.key == pygame.K_5:
                    difficulty = "nightmare"
                if difficulty:
                    game_state = "playing"

    window.fill(background_color)

    if game_state == "menu":
        draw_menu()

    elif game_state == "difficulty":
        draw_difficulty()

    elif game_state == "playing":
        left_bar.action()
        right_bar.action(ball)
        ball.action()

        if pygame.sprite.collide_rect(ball, left_bar):
            ball.speed_x *= -1

        if pygame.sprite.collide_rect(ball, right_bar):
            ball.speed_x *= -1

        if ball.rect.x <= 0:
            game_state = "gameover"
            loser_text = "PLAYER 1 LOSE"

        if ball.rect.x >= 700 - ball.rect.width:
            game_state = "gameover"
            loser_text = "PLAYER 2 LOSE"

        left_bar.reset()
        right_bar.reset()
        ball.reset()

    elif game_state == "gameover":
        if loser_text == "PLAYER 1 LOSE":
            window.blit(lose1, (200, 230))
        else:
            window.blit(lose2, (200, 230))

    pygame.display.update()
    game_clock.tick(FPS)

pygame.quit()