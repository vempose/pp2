import pygame
import sys
import random
from pygame.locals import *

pygame.init()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/racer/enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600: # if off the screen at the bottom
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/racer/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520) # initial position of the player

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Controls with well-known WASD layout
        if self.rect.left > 0:
            if pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:
            if pressed_keys[K_d]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/racer/coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.respawn()

    # Set self position somewhere at the very top
    def respawn(self):
        self.rect.top = 0
        self.rect.center = (random.randint(self.rect.width, WIDTH - self.rect.width), 0)

    def move(self):
        # Add some randomness to coin moving speed
        self.rect.move_ip(0, SPEED + random.randint(0, 3))
        if self.rect.top > 600:
            self.respawn()


# Game variables
WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0
MONEY = 0

# Core variables and configuration
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("images/racer/background.png").convert()
pygame.display.set_caption("Racer Game")

P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
enemies.add(E1)
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Working with fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, pygame.Color("black"))

# Adding a new User event for speed increasing
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 8000)

while True:
    clock.tick(60)
    # Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # An intuitive way to get out of the game
    if pygame.key.get_pressed()[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Preparing text surfaces
    scores = font_small.render(str(SCORE), True, pygame.Color("white"))
    money = font_small.render(str(MONEY), True, pygame.Color("yellow"))
    # Rendering surfaces
    display_surface.blit(background, (0, 0))
    display_surface.blit(scores, (30, 10))
    display_surface.blit(money, (WIDTH - 43, 10))

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        display_surface.fill("red")
        display_surface.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        # Press ESCAPE to exit the game (steady red screen)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if pygame.key.get_pressed()[K_ESCAPE]:
                pygame.quit()
                sys.exit()

    # Increment coin counter when colliding with player
    if pygame.sprite.spritecollideany(P1, coins):
        MONEY += 1
        for coin in coins:
            coin.respawn()

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        display_surface.blit(entity.image, entity.rect)
        entity.move()

    pygame.display.update()
