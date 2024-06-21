import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128)   # Purple
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

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
    [[1, 1, 1], [0, 0, 1]]   # J shape
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


def main():
    grid = create_grid()
    current_tetromino = Tetromino(random.choice(SHAPES))
    next_tetromino = Tetromino(random.choice(SHAPES))
    drop_time = 0
    drop_interval = 500  # milliseconds
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.y -= 1
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if check_collision(grid, current_tetromino):
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()

        drop_time += clock.get_rawtime()
        clock.tick()

        if drop_time > drop_interval:
            drop_time = 0
            current_tetromino.y += 1
            if check_collision(grid, current_tetromino):
                current_tetromino.y -= 1
                lock_tetromino(grid, current_tetromino)
                clear_lines(grid)
                current_tetromino = next_tetromino
                next_tetromino = Tetromino(random.choice(SHAPES))
                if check_collision(grid, current_tetromino):
                    game_over = True

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetromino(screen, current_tetromino)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

