import pygame

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball")

ball_radius = 25
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed = 20

running = True
while running:
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # WASD controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and ball_x - ball_radius - ball_speed >= 0:
        ball_x -= ball_speed
    if keys[pygame.K_d] and ball_x + ball_radius + ball_speed <= WIDTH:
        ball_x += ball_speed
    if keys[pygame.K_w] and ball_y - ball_radius - ball_speed >= 0:
        ball_y -= ball_speed
    if keys[pygame.K_s] and ball_y + ball_radius + ball_speed <= HEIGHT:
        ball_y += ball_speed

    pygame.draw.circle(screen, "red", (ball_x, ball_y), ball_radius)
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
