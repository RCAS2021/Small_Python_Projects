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

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        # Getting what power of 2 the tile value is and subtract 1
        color_index = int(math.log2(self.value) - 1)
        # Select color based on color index
        color = self.COLORS[color_index]
        return color

    def draw_tile(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        # Creating a surface for the text
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        # Put a surface on the screen
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self):
        pass

    def move(self, delta):
        pass



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

def draw(window, tiles):
    # Changing background color
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw_tile(window)

    draw_grid(window)

    pygame.display.update()

def get_random_pos(tiles):
    row = None
    col = None

    # Continue generating unless new tile
    while True:
        # Generating xy
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLUMNS)

        # Checking if tile already exists
        if f"{row}{col}" not in tiles:
            break

    return row, col

def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(window):
    # Setting game speed
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        # Creating quit event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, tiles)


    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)

