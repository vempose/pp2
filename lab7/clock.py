import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock")

clock_face = pygame.image.load("images/clock.png")
clock_rect = clock_face.get_rect(center = (WIDTH // 2, HEIGHT // 2))

sec_hand = pygame.image.load("images/sec_hand.png")
sec_rect = sec_hand.get_rect(center = (WIDTH // 2, HEIGHT // 2))

min_hand = pygame.image.load("images/min_hand.png")
min_rect = min_hand.get_rect(center = (WIDTH // 2, HEIGHT // 2))


running = True
while running:
    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute

    sec_correct_angle = 56
    sec_angle = -seconds * 6 + sec_correct_angle

    min_correct_angle = 52
    min_angle = -minutes * 6 - min_correct_angle  

    rotated_sec = pygame.transform.rotate(sec_hand, sec_angle)
    rotated_sec_rect = rotated_sec.get_rect(center = sec_rect.center)

    rotated_min = pygame.transform.rotate(min_hand, min_angle)
    rotated_min_rect = rotated_min.get_rect(center = min_rect.center)

    screen.fill("white")
    screen.blit(clock_face, clock_rect)
    screen.blit(rotated_min, rotated_min_rect)
    screen.blit(rotated_sec, rotated_sec_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
