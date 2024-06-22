import pygame
import random
import json

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Convert hex color to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

#Grid 
def draw_grid_lines(surface):
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(surface, COLOR_PALETTE['WHITE'], (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(surface, COLOR_PALETTE['WHITE'], (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)



def draw_grid_lines(surface):
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(surface, COLOR_PALETTE['WHITE'], (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(surface, COLOR_PALETTE['WHITE'], (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE

# Color palette
COLOR_PALETTE = {key: hex_to_rgb(value) for key, value in config['color_palette'].items()}
BLACK = COLOR_PALETTE['BLACK']

# Colors for tetrominoes
COLORS = [COLOR_PALETTE['CYAN'], COLOR_PALETTE['RED'], COLOR_PALETTE['GREEN'], COLOR_PALETTE['BLUE'],
          COLOR_PALETTE['YELLOW'], COLOR_PALETTE['ORANGE'], COLOR_PALETTE['PURPLE']]

# Initialize Pygame
pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Font for displaying FPS
font = pygame.font.SysFont('Arial', 18)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]]  # J shape
]

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid():
    return [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_tetromino(surface, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color, ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def check_collision(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetromino.y + y >= GRID_HEIGHT or
                    tetromino.x + x < 0 or
                    tetromino.x + x >= GRID_WIDTH or
                    grid[tetromino.y + y][tetromino.x + x] != BLACK):
                    return True
    return False

def lock_tetromino(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines(grid):
    lines_cleared = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        if all(cell != BLACK for cell in grid[y]):
            del grid[y]
            grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    return lines_cleared

def draw_fps(surface, clock):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, COLOR_PALETTE['WHITE'])
    surface.blit(fps_text, (10, 10))

def main():
    grid = create_grid()
    current_tetromino = Tetromino(random.choice(SHAPES))
    next_tetromino = Tetromino(random.choice(SHAPES))
    drop_time = 0
    drop_interval = 500  # milliseconds
    game_over = False
    paused = False
    lines_cleared = 0

    key_mapping = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'down': pygame.K_DOWN,
        'up': pygame.K_UP,
        'space': pygame.K_SPACE,
        'z': pygame.K_z
    }

    controls = {
        'rotate': key_mapping[config["controls"]["rotate"]],
        'left': key_mapping[config["controls"]["left"]],
        'right': key_mapping[config["controls"]["right"]],
        'down': key_mapping[config["controls"]["down"]],
        'drop': key_mapping[config["controls"]["drop"]],
        'pause': key_mapping[config["controls"]["pause"]]
    }

    key_hold_time = {
        'left': 0,
        'right': 0,
        'down': 0
    }

    key_repeat_delay = 200  # milliseconds
    key_repeat_interval = 50  # milliseconds

    while not game_over:
        dt = clock.tick(60)
        drop_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == controls['pause']:
                    paused = not paused
                if not paused:
                    if event.key == controls['left']:
                        key_hold_time['left'] = pygame.time.get_ticks()
                        current_tetromino.x -= 1
                        if check_collision(grid, current_tetromino):
                            current_tetromino.x += 1
                    elif event.key == controls['right']:
                        key_hold_time['right'] = pygame.time.get_ticks()
                        current_tetromino.x += 1
                        if check_collision(grid, current_tetromino):
                            current_tetromino.x -= 1
                    elif event.key == controls['down']:
                        key_hold_time['down'] = pygame.time.get_ticks()
                        current_tetromino.y += 1
                        if check_collision(grid, current_tetromino):
                            current_tetromino.y -= 1
                    elif event.key == controls['drop']:
                        while not check_collision(grid, current_tetromino):
                            current_tetromino.y += 1
                        current_tetromino.y -= 1
                        lock_tetromino(grid, current_tetromino)
                        lines_cleared += clear_lines(grid)
                        current_tetromino = next_tetromino
                        next_tetromino = Tetromino(random.choice(SHAPES))
                        if check_collision(grid, current_tetromino):
                            game_over = True
                    elif event.key == controls['rotate']:
                        current_tetromino.rotate()
                        if check_collision(grid, current_tetromino):
                            current_tetromino.rotate()
                            current_tetromino.rotate()
                            current_tetromino.rotate()
            elif event.type == pygame.KEYUP:
                if event.key in controls.values():
                    key_hold_time['left'] = 0
                    key_hold_time['right'] = 0
                    key_hold_time['down'] = 0

        if not paused:
            for key in ['left', 'right', 'down']:
                if key_hold_time[key] > 0:
                    current_time = pygame.time.get_ticks()
                    if current_time - key_hold_time[key] > key_repeat_delay:
                        if (current_time - key_hold_time[key]) % key_repeat_interval < dt:
                            if key == 'left':
                                current_tetromino.x -= 1
                                if check_collision(grid, current_tetromino):
                                    current_tetromino.x += 1
                            elif key == 'right':
                                current_tetromino.x += 1
                                if check_collision(grid, current_tetromino):
                                    current_tetromino.x -= 1
                            elif key == 'down':
                                current_tetromino.y += 1
                                if check_collision(grid, current_tetromino):
                                    current_tetromino.y -= 1

            if drop_time > drop_interval:
                drop_time = 0
                current_tetromino.y += 1
                if check_collision(grid, current_tetromino):
                    current_tetromino.y -= 1
                    lock_tetromino(grid, current_tetromino)
                    lines_cleared += clear_lines(grid)
                    current_tetromino = next_tetromino
                    next_tetromino = Tetromino(random.choice(SHAPES))
                    if check_collision(grid, current_tetromino):
                        game_over = True

            if lines_cleared >= 5:
                lines_cleared = 0
                drop_interval = max(50, drop_interval - 50)

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_grid_lines(screen)  # Add this line to draw the grid lines
        draw_tetromino(screen, current_tetromino)
        draw_fps(screen, clock)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()