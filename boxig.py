import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'graphics/player1/playertest.png').convert_alpha()
        self.rect = self.image.get_rect(center=(200, 300))

    def player_input(self):
        left, right, up, down = CollisionType()
        vel = 6
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and up:
            self.rect.y -= vel
        if keys[pygame.K_DOWN] and down:
            self.rect.y += vel
        if keys[pygame.K_LEFT] and left:
            self.rect.x -= vel
        if keys[pygame.K_RIGHT] and right:
            self.rect.x += vel
        if keys[pygame.K_SPACE]:
            pass

    def bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600

    def update(self):
        self.player_input()
        self.bounds()


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(
            'graphics/player2/playertest2.png').convert_alpha()
        self.rect = self.image.get_rect(center=(600, 300))

    def player_input(self):
        right, left, down, up = CollisionType()
        vel = 6
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and up:
            self.rect.y -= vel
        if keys[pygame.K_s] and down:
            self.rect.y += vel
        if keys[pygame.K_a] and left:
            self.rect.x -= vel
        if keys[pygame.K_d] and right:
            self.rect.x += vel

    def bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600

    def update(self):
        self.player_input()
        self.bounds()


def CollisionType():
    left, right, up, down = True, True, True, True
    tollerance= 8
    if pygame.sprite.collide_rect(player.sprite, player2.sprite):
        if abs(player.sprite.rect.right - player2.sprite.rect.left) < 8:
            right = False
        if abs(player.sprite.rect.left - player2.sprite.rect.right) < 8:
            left = False
        if abs(player.sprite.rect.top - player2.sprite.rect.bottom) < 8:
            up = False
        if abs(player.sprite.rect.bottom - player2.sprite.rect.top) < 8:
            down = False
    return left, right, up, down


def Temporizador():
    time = pygame.time.get_ticks() // 1000 - round_start
    round_time = 120 - time
    minuts = round_time // 60
    secs = round_time % 60
    time_surf = font.render(f'{minuts}:{secs:02d}', False, "Pink")
    time_rec = time_surf.get_rect(center=(400, 50))
    screen.blit(time_surf, time_rec)
    return round_time


def Draw():
    if player.sprite.rect.x < player2.sprite.rect.x:
        player.sprite.image = pygame.image.load(
            'graphics/player1/playertest.png').convert_alpha()
        player2.sprite.image = pygame.image.load(
            'graphics/player2/playertest2.png').convert_alpha()
        
    else:
        player.sprite.image = pygame.image.load(
            'graphics/player1/playertestinv.png').convert_alpha()
        player2.sprite.image = pygame.image.load(
            'graphics/player2/playertest2inv.png').convert_alpha()


pygame.init()

# Window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Boxing')

# Font
font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Mensagens
message = font.render("Press Space to Start", False, "Pink")
message_rect = message.get_rect(center=(400, 400))
messagD = font.render("Draw!", False, "Pink")
messagD_rect = messagD.get_rect(center=(400, 300))
messagB = font.render("Black wins!", False, "Black")
messagB_rect = messagB.get_rect(center=(400, 300))
messagW = font.render("White wins!", False, "White")
messagW_rect = messagW.get_rect(center=(400, 300))

# Clock
clock = pygame.time.Clock()

# Game State
running = False

# Sprite 1
player = pygame.sprite.GroupSingle()
player.add(Player())
# Sprite 2
player2 = pygame.sprite.GroupSingle()
player2.add(Player2())

# Temporizador
round_start = 0

# Flag para display de ganhou ou n
flag = False

while True:
    for event in pygame.event.get():
        # sair do jogo
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                running = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flag = True
                player.sprite.rect.center = (200, 300)
                player2.sprite.rect.center = (600, 300)
                round_start = pygame.time.get_ticks() // 1000
                scoreW, scoreB = 0, 0
                running = True

    if running:
        # Logic
        player.update()
        player2.update()
        Draw()

        if Temporizador() == 0 or scoreW == 100 or scoreB == 100:
            running = False

        # Draw
        scoreW_sur = font.render(f'Score: {scoreW}', False, "White")
        scoreW_rect = scoreW_sur.get_rect(center=(700, 50))
        scoreB_sur = font.render(f'Score: {scoreB}', False, "Black")
        scoreB_rect = scoreB_sur.get_rect(center=(100, 50))

        screen.fill(pygame.Color((108, 152, 80)))
        player.draw(screen)
        player2.draw(screen)
        screen.blit(scoreW_sur, scoreW_rect)
        screen.blit(scoreB_sur, scoreB_rect)
        Temporizador()

    else:
        screen.fill(pygame.Color((108, 152, 80)))
        if flag:
            if scoreW == scoreB:
                screen.blit(messagD, messagD_rect)
            elif scoreW > scoreB:
                screen.blit(messagW, messagW_rect)
            else:
                screen.blit(messagB, messagB_rect)
        screen.blit(message, message_rect)
        pass

    # Update do display
    pygame.display.update()
    clock.tick(60)
