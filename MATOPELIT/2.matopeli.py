import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set up the game clock
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the snake
snake_size = 20
snake_speed = 10
snake_x = width // 2
snake_y = height // 2
snake_dx = 0
snake_dy = 0
snake_body = []
snake_length = 1

# Set up the food
food_size = 20
food_x = random.randint(0, width - food_size) // 20 * 20
food_y = random.randint(0, height - food_size) // 20 * 20

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -snake_size
                snake_dy = 0
            elif event.key == pygame.K_RIGHT:
                snake_dx = snake_size
                snake_dy = 0
            elif event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -snake_size
            elif event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = snake_size

    # Update snake position
    snake_x += snake_dx
    snake_y += snake_dy

    # Wrap snake around the screen
    if snake_x < 0:
        snake_x = width - snake_size
    elif snake_x >= width:
        snake_x = 0
    if snake_y < 0:
        snake_y = height - snake_size
    elif snake_y >= height:
        snake_y = 0

    # Check for collision with food
    if snake_x == food_x and snake_y == food_y:
        food_x = random.randint(0, width - food_size) // 20 * 20
        food_y = random.randint(0, height - food_size) // 20 * 20
        snake_length += 1

    # Update snake body
    snake_body.append((snake_x, snake_y))
    if len(snake_body) > snake_length:
        del snake_body[0]

    # Check for collision with snake body
    if (snake_x, snake_y) in snake_body[:-1]:
        running = False

    # Clear the window
    window.fill(BLACK)

    # Draw snake
    for segment in snake_body:
        pygame.draw.rect(window, GREEN, (segment[0], segment[1], snake_size, snake_size))

    # Draw food
    pygame.draw.rect(window, RED, (food_x, food_y, food_size, food_size))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(snake_speed)

# Quit the game
pygame.quit()