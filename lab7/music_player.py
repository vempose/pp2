import pygame
import os
import sys

pygame.init()

# Load music
MUSIC_FOLDER = "music"
tracks = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
if not tracks:
    print("No mp3 files found in 'music' folder.")
    sys.exit()

current_track = 0
paused_time = 0
is_paused = False

def play_track(index):
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, tracks[index]))
    pygame.mixer.music.play()
    print(f"Now playing: {tracks[index]}")

play_track(current_track)

# Setup display (required to capture key events)
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Simple Music Player")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    paused_time = pygame.mixer.music.get_pos() / 1000.0
                    pygame.mixer.music.stop()
                    print(f"Paused at {paused_time:.2f} sec")
                    is_paused = True
                else:
                    pygame.mixer.music.play(start = paused_time)
                    print(f"Resumed from {paused_time:.2f} sec")
                    paused_time = 0

            elif event.key == pygame.K_p:
                current_track = (current_track - 1) % len(tracks)
                play_track(current_track)
                is_paused = False

            elif event.key == pygame.K_n:
                current_track = (current_track + 1) % len(tracks)
                play_track(current_track)
                is_paused = False

            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                running = False

    pygame.time.Clock().tick(30)
pygame.quit()
