import pygame
import sys
import random

pygame.init()
pygame.display.set_caption('Simple Snake')

# System vars
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Game's logic var
snake_pos = [250, 250]
snake_body = [[250, 250], [240, 250], [230, 250]]
actual_direction = 'RIGHT'
future_direction = actual_direction
score = 0
level = 1
speed = 5

# Font
font = pygame.font.SysFont('Consolas', 20)

def generate_food():
    while True:
        food_x = random.randrange(0, WIDTH, CELL_SIZE)
        food_y = random.randrange(0, HEIGHT, CELL_SIZE)
        if [food_x, food_y] not in snake_body:
            return [food_x, food_y]

food_pos = generate_food()

running = True
while running:
    # Determining direction of movement (WASD controls)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and actual_direction != 'DOWN':
                future_direction = 'UP'
            elif event.key == pygame.K_s and actual_direction != 'UP':
                future_direction = 'DOWN'
            elif event.key == pygame.K_d and actual_direction != 'LEFT':
                future_direction = 'RIGHT'
            elif event.key == pygame.K_a and actual_direction != 'RIGHT':
                future_direction = 'LEFT'
    actual_direction = future_direction

    # Movement
    if actual_direction == 'UP':
        snake_pos[1] -= CELL_SIZE
    elif actual_direction == 'DOWN':
        snake_pos[1] += CELL_SIZE
    elif actual_direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE
    elif actual_direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE

    # Collision with wall (teleport)
    if snake_pos[0] < 0:
        snake_pos[0] = WIDTH - CELL_SIZE
    elif snake_pos[0] >= WIDTH:
        snake_pos[0] = 0
    elif snake_pos[1] < 0:
        snake_pos[1] = HEIGHT - CELL_SIZE
    elif snake_pos[1] >= HEIGHT:
        snake_pos[1] = 0

    # Snake growth (level increases with every 4 foods)
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        if score % 4 == 0:
            level += 1
            speed += 2
        food_pos = generate_food()
    else:
        snake_body.pop()

    # Check collision with itself
    if snake_pos in snake_body[3:]:
        running = False

    # Rendering
    screen.fill(black)
    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    # Score and level counters
    score_text = font.render(f'Score: {score}  Level: {level}', True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

# Clean exit
pygame.quit()
sys.exit()
