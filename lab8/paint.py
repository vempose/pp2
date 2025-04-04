import pygame
import sys

# Initialization
pygame.init()
pygame.display.set_caption("Simple Paint")

# System config
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Drawing state
drawing = False
brush_color = BLACK
tool = "brush"

# Interface vars
TOOLBAR_HEIGHT = 50
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 30
BUTTON_PADDING = 10

font = pygame.font.SysFont("Consolas", 18)

# Configuring button
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_color = WHITE if self.color != GRAY else BLACK
        text_surface = font.render(self.text, True, text_color)
        screen.blit(text_surface, (self.rect.x + 8, self.rect.y + 6))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

def set_tool(selected_tool):
    global tool
    tool = selected_tool

def set_color(color):
    global brush_color
    brush_color = color

def clear_screen():
    screen.fill(WHITE)

def exit_app():
    pygame.quit()
    sys.exit()

# Init background
clear_screen()

# Buttons setup
buttons = []
button_defs = [
    ("Black", BLACK, lambda: set_color(BLACK)),
    ("Green", GREEN, lambda: set_color(GREEN)),
    ("Red", RED, lambda: set_color(RED)),
    ("Blue", BLUE, lambda: set_color(BLUE)),
    ("Brush", GRAY, lambda: set_tool("brush")),
    ("Rect", GRAY, lambda: set_tool("rect")),
    ("Circle", GRAY, lambda: set_tool("circle")),
    ("Eraser", GRAY, lambda: set_tool("eraser")),
]

# Buttons positioning
x_pos = BUTTON_PADDING
for text, color, action in button_defs:
    buttons.append(Button(x_pos, 10, BUTTON_WIDTH, BUTTON_HEIGHT, text, color, action))
    x_pos += BUTTON_WIDTH + BUTTON_PADDING

# Clear and Exit buttons at the very right
buttons.append(Button(WIDTH - 140, 10, 60, BUTTON_HEIGHT, "Clear", GRAY, clear_screen))
buttons.append(Button(WIDTH - 70, 10, 60, BUTTON_HEIGHT, "Exit", GRAY, exit_app))

start_pos = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_app()

        for button in buttons:
            button.check_action(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y > TOOLBAR_HEIGHT:
                drawing = True
                start_pos = (mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and start_pos and tool in ["rect", "circle"]:
                end_pos = pygame.mouse.get_pos()
                color = WHITE if tool == "eraser" else brush_color

                if tool == "rect":
                    x, y = start_pos
                    w = end_pos[0] - x
                    h = end_pos[1] - y
                    pygame.draw.rect(screen, color, (x, y, w, h), 2)
                elif tool == "circle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)

            drawing = False
            start_pos = None

    # Eraser and brush logic
    if drawing and tool in ["brush", "eraser"]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > TOOLBAR_HEIGHT:
            color = WHITE if tool == "eraser" else brush_color
            pygame.draw.circle(screen, color, (mouse_x, mouse_y), 5)

    # Draw toolbar background and buttons
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    for button in buttons:
        button.draw()

    pygame.display.flip()
