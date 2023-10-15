import pygame
import random 

# Set up the game board size
WIDTH = HEIGHT = 800
NUM_TILES = 40
UNIT = HEIGHT / NUM_TILES
# Make sure that the grid is evenly tileable
assert(WIDTH % NUM_TILES == 0)

# WASD movement (0: forward, 1: left, 2: backwards, 3: right)
direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]

# RGB colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Start pygame and clock
pygame.init()
clock = pygame.time.Clock()
# Randomly found FPS that seems to be okay in relation to num tiles.
FPS = NUM_TILES / 3

# Set up game window and caption
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Returns a random apple position on a board tile (x, y).
def random_apple() -> (int, int):
    x_pos = random.randint(0, NUM_TILES - 1) * UNIT
    y_pos = random.randint(0, NUM_TILES - 1) * UNIT
    return (x_pos, y_pos)

# Draws the apple and snake on the board
def draw(apple_pos, snake):
    pygame.draw.rect(window, red, (apple_pos[0], apple_pos[1], UNIT, UNIT))
    for (x,y) in snake:
        pygame.draw.rect(window, white, (x, y, UNIT, UNIT))

# Moves the snake based on a direction list that corresponds 1:1 with the snake.
def move(snake, body_dir):
    for i in range(len(snake)):
        x,y = snake[i]
        x_dir, y_dir = body_dir[i]
        snake[i] = (x + UNIT * x_dir, y + UNIT * y_dir)

# Checks if the snake is on the board
def in_bounds(snake) -> bool:
    for (x,y) in snake:
        if not 0 <= x < WIDTH or not 0 <= y < HEIGHT:
            return False
    return True

# Checks if the snake has "eaten" the apple
def check_apple(snake, apple):
    return snake[0] == apple

# Chains the body direction. Changes 1 body part a time (per frame).
def chain_dir(body_dir):
    if len(body_dir) == 2 and body_dir[0] != body_dir[1]:
        body_dir[1] = body_dir[0]
    else:
        for i in range(len(body_dir) - 1):
            if body_dir[i + 1] != body_dir[i]:
                body_dir[i + 1] = body_dir[i]
                break

# Checks if the snake has collided with itself (duplicate position coordinates).
def collision(snake) -> bool:
    return len(snake) != len(set(snake))

# Set up initial apple and snake position/direction.
apple = random_apple()
snake = [((NUM_TILES / 2) * UNIT, (NUM_TILES / 2) * UNIT)]
body_dir = [direction[3]]

# Start game loop
running = True
chain = False
while running:
    # Make sure only 1 directional input per frame
    button_already_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN and not button_already_pressed:
            button = event.key
            # Check if W is first pressed. If so, go forwards and chain (1 == head moves, 0 == body moves).
            if button == pygame.K_w and body_dir[0] != direction[2]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[0]
                chain = True
            # Check if A is first pressed.
            elif button == pygame.K_a and body_dir[0] != direction[3]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[1]
                chain = True
            # Check if S is first pressed.
            elif button == pygame.K_s and body_dir[0] != direction[0]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[2]
                chain = True
            # Check if D is first pressed.
            elif button == pygame.K_d and body_dir[0] != direction[1]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[3]
                chain = True

    # Check for apple colision. If you hit apple, add body segment at end of snake.
    # Get new apple.
    if check_apple(snake, apple):
        a_x, a_y = apple
        tail_x, tail_y = snake[-1]
        x_dir, y_dir = body_dir[-1]
        snake.append((tail_x - UNIT * x_dir, tail_y - UNIT * y_dir))
        body_dir.append((x_dir, y_dir))
        apple = random_apple()

    # Check if snake is out of bounds of has collided with itself.
    if not in_bounds(snake) or collision(snake):
        running = False
        break
    
    # Chain the frame after head has been updated.
    if not chain:
        chain_dir(body_dir)
    window.fill(black)
    move(snake, body_dir)
    draw(apple, snake)

    # Change back to False (if the head made it True then here it has passed a frame
    # of drawing so you can chain now.)
    chain = False

    # Limit frame rate and update the board.
    clock.tick(FPS)
    pygame.display.flip()

# Game over.
window.fill(red)
pygame.display.flip()
pygame.time.delay(1500)
