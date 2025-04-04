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
TOOLBAR_HEIGHT = 90
BUTTON_WIDTH = 70
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

    def draw(self, screen):
        # Draw rounded rectangle with border
        pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=8)  # border color
        pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4), border_radius=6)

        # Render centered text
        font = pygame.font.SysFont("Consolas", 16, bold=True)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

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
    ("Eraser", GRAY, lambda: set_tool("eraser")),
    ("Rect", GRAY, lambda: set_tool("rect")),
    ("Circle", GRAY, lambda: set_tool("circle")),
    ("Square", GRAY, lambda: set_tool("square")),
    ("R. Tri", GRAY, lambda: set_tool("right_triangle")),
    ("E. Tri", GRAY, lambda: set_tool("equilateral_triangle")),
    ("Rhombus", GRAY, lambda: set_tool("rhombus")),
]

# Buttons positioning
x_pos = BUTTON_PADDING
y_offset = 10
for i, (text, color, action) in enumerate(button_defs):
    if i == 6:  # make second row after 6 buttons
        x_pos = BUTTON_PADDING
        y_offset = 50
    buttons.append(Button(x_pos, y_offset, BUTTON_WIDTH, BUTTON_HEIGHT, text, color, action))
    x_pos += BUTTON_WIDTH + BUTTON_PADDING

# Clear and Exit buttons at far right
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
            if drawing and start_pos and tool in ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
                end_pos = pygame.mouse.get_pos()
                x1, y1 = start_pos
                x2, y2 = end_pos
                color = WHITE if tool == "eraser" else brush_color

                if tool == "rect":
                    pygame.draw.rect(screen, color, pygame.Rect(x1, y1, x2 - x1, y2 - y1), 2)

                elif tool == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(screen, color, pygame.Rect(x1, y1, side, side), 2)

                elif tool == "circle":
                    radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)

                elif tool == "right_triangle":
                    points = [start_pos, (x1, y2), (x2, y2)]
                    pygame.draw.polygon(screen, color, points, 2)

                elif tool == "equilateral_triangle":
                    side = abs(x2 - x1)
                    height = side * (3 ** 0.5) / 2
                    direction = -1 if y2 < y1 else 1
                    points = [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side / 2, y1 + direction * height)
                    ]
                    pygame.draw.polygon(screen, color, points, 2)

                elif tool == "rhombus":
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
                    pygame.draw.polygon(screen, color, points, 2)

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
        button.draw(screen)

    pygame.display.flip()
