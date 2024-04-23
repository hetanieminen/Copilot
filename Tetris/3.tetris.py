import pygame
import random

# Initialize the game
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Define the Tetris grid
grid_size = 30
grid_width = window_width // grid_size
grid_height = window_height // grid_size
grid = [[BLACK] * grid_width for _ in range(grid_height)]

# Define the Tetriminos
tetriminos = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]]  # J
]

# Define the current Tetrimino
current_tetrimino = random.choice(tetriminos)
current_tetrimino_x = grid_width // 2 - len(current_tetrimino[0]) // 2
current_tetrimino_y = 0

# Game loop
running = True
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5

def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(window, grid[y][x], (x * grid_size, y * grid_size, grid_size, grid_size))

def draw_tetrimino():
    for y in range(len(current_tetrimino)):
        for x in range(len(current_tetrimino[y])):
            if current_tetrimino[y][x] == 1:
                pygame.draw.rect(window, WHITE, ((current_tetrimino_x + x) * grid_size, (current_tetrimino_y + y) * grid_size, grid_size, grid_size))

def check_collision():
    for y in range(len(current_tetrimino)):
        for x in range(len(current_tetrimino[y])):
            if current_tetrimino[y][x] == 1:
                if current_tetrimino_y + y >= grid_height or current_tetrimino_x + x < 0 or current_tetrimino_x + x >= grid_width or grid[current_tetrimino_y + y][current_tetrimino_x + x] != BLACK:
                    return True
    return False

def merge_tetrimino():
    for y in range(len(current_tetrimino)):
        for x in range(len(current_tetrimino[y])):
            if current_tetrimino[y][x] == 1:
                grid[current_tetrimino_y + y][current_tetrimino_x + x] = WHITE

def remove_completed_rows():
    completed_rows = []
    for y in range(grid_height):
        if all(color != BLACK for color in grid[y]):
            completed_rows.append(y)
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [BLACK] * grid_width)

def handle_user_input():
    global current_tetrimino_x, current_tetrimino_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        current_tetrimino_x -= 1
        if check_collision():
            current_tetrimino_x += 1
    if keys[pygame.K_RIGHT]:
        current_tetrimino_x += 1
        if check_collision():
            current_tetrimino_x -= 1
    if keys[pygame.K_DOWN]:
        current_tetrimino_y += 1
        if check_collision():
            current_tetrimino_y -= 1
    if keys[pygame.K_SPACE]:
        while not check_collision():
            current_tetrimino_y += 1
        current_tetrimino_y -= 1

def update_game_logic():
    global current_tetrimino_x, current_tetrimino_y, current_tetrimino, fall_time, running
    fall_time += clock.get_rawtime()
    if fall_time / 1000 >= fall_speed:
        current_tetrimino_y += 1
        if check_collision():
            current_tetrimino_y -= 1
            merge_tetrimino()
            remove_completed_rows()
            if current_tetrimino_y == 0:
                running = False
            else:
                current_tetrimino = random.choice(tetriminos)
                current_tetrimino_x = grid_width // 2 - len(current_tetrimino[0]) // 2
                current_tetrimino_y = 0
        fall_time = 0

def render_game():
    window.fill(BLACK)
    draw_grid()
    draw_tetrimino()

def update_display():
    pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_user_input()
    update_game_logic()
    render_game()
    update_display()

    clock.tick(60)

# Game over
pygame.quit()