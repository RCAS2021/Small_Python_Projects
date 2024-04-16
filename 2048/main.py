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

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

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
        # Generating row, col
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLUMNS)

        # Checking if tile already exists
        if f"{row}{col}" not in tiles:
            break

    return row, col

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    # Handling directions
    if direction == "left":
        # Gets columns
        sort_func = lambda x: x.col
        reverse = False
        # Sets velocity
        delta = (-MOVE_VELOCITY, 0)
        # Checking if it's on the boundary
        boundary_check = lambda tile: tile.col == 0
        # Get tile to the left
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        # Checking if the tile should be merged
        # Checks if after moving, the tile is overlapping the other
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VELOCITY
        # Checks if tile doesn't have same value, move to the border of the next tile
        move_check = (lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VELOCITY)
        # Round up
        ceil = True
    elif direction == "right":
        # Gets columns
        sort_func = lambda x: x.col
        reverse = True
        # Sets velocity
        delta = (MOVE_VELOCITY, 0)
        # Checking if it's on the boundary
        boundary_check = lambda tile: tile.col == COLUMNS - 1
        # Get tile to the left
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        # Checking if the tile should be merged
        # Checks if after moving, the tile is overlapping the other
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VELOCITY
        # Checks if tile doesn't have same value, move to the border of the next tile
        move_check = (lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VELOCITY < next_tile.x)
        # Round up
        ceil = False
    elif direction == "up":
        # Gets columns
        sort_func = lambda x: x.row
        reverse = False
        # Sets velocity
        delta = (0, -MOVE_VELOCITY)
        # Checking if it's on the boundary
        boundary_check = lambda tile: tile.row == 0
        # Get tile to the left
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        # Checking if the tile should be merged
        # Checks if after moving, the tile is overlapping the other
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VELOCITY
        # Checks if tile doesn't have same value, move to the border of the next tile
        move_check = (lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VELOCITY)
        # Round up
        ceil = True
    elif direction == "down":
    
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        # Iterating through tiles
        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            
            # Getting next tile
            next_tile = get_next_tile(tile)
            # If there isn't a next tile, move
            if not next_tile:
                tile.move(delta)
            # If tile and next tile have the same value and not already merged
            elif (tile.value == next_tile.value and tile not in blocks and next_tile not in blocks):
                # Merge
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            # Move until border reached
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True
        
        update_tiles(window, tiles, sorted_tiles)
    
    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "Game Ended"
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "Continue"

def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    
    draw(window, tiles)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
