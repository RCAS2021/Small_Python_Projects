import pygame
import random
import math

# Initialize pygame
pygame.init()

# Defining constants
FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLUMNS = 4
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLUMNS
OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

# Creating window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# Setting caption
pygame.display.set_caption("2048")
# Setting font
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
# Velocity of rectangles movement
MOVE_VELOCITY = 20

def draw_grid(window):
    # Drawing horizontal lines
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    # Drawing vertical lines
    for col in range(1, ROWS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)


    # Drawing border
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window):
    # Changing background color
    window.fill(BACKGROUND_COLOR)

    draw_grid(window)

    pygame.display.update()

def main(window):
    # Setting game speed
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        # Creating quit event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window)


    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)

