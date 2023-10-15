import pygame
import random 

WIDTH = HEIGHT = 800
NUM_TILES = 40
UNIT = HEIGHT / NUM_TILES
# Make sure that the grid is evenly tileable
assert(WIDTH % NUM_TILES == 0)

# WASD movement
direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
clock = pygame.time.Clock()
FPS = NUM_TILES / 3

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

def random_apple() -> (int, int):
    x_pos = random.randint(0, NUM_TILES - 1) * UNIT
    y_pos = random.randint(0, NUM_TILES - 1) * UNIT
    return (x_pos, y_pos)

def draw(apple_pos, snake):
    pygame.draw.rect(window, red, (apple_pos[0], apple_pos[1], UNIT, UNIT))
    for (x,y) in snake:
        pygame.draw.rect(window, white, (x, y, UNIT, UNIT))

def move(snake, body_dir):
    for i in range(len(snake)):
        x,y = snake[i]
        x_dir, y_dir = body_dir[i]
        snake[i] = (x + UNIT * x_dir, y + UNIT * y_dir)

def in_bounds(snake) -> bool:
    for (x,y) in snake:
        if not 0 <= x < WIDTH or not 0 <= y < HEIGHT:
            return False
    return True

def check_apple(snake, apple):
    return snake[0] == apple

def chain_dir(body_dir):
    if len(body_dir) == 2 and body_dir[0] != body_dir[1]:
        body_dir[1] = body_dir[0]
    else:
        for i in range(len(body_dir) - 1):
            if body_dir[i + 1] != body_dir[i]:
                body_dir[i + 1] = body_dir[i]
                break

def collision(snake) -> bool:
    return len(snake) != len(set(snake))

apple = random_apple()
snake = [((NUM_TILES / 2) * UNIT, (NUM_TILES / 2) * UNIT)]
body_dir = [direction[3]]

running = True
chain = False
prev_time = clock.get_time()
while running:
    button_already_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN and not button_already_pressed:
            button = event.key
            if button == pygame.K_w and body_dir[0] != direction[2]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[0]
                chain = True
            elif button == pygame.K_a and body_dir[0] != direction[3]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[1]
                chain = True
            elif button == pygame.K_s and body_dir[0] != direction[0]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[2]
                chain = True
            elif button == pygame.K_d and body_dir[0] != direction[1]:
                button_already_pressed = not button_already_pressed
                body_dir[0] = direction[3]
                chain = True

    if check_apple(snake, apple):
        a_x, a_y = apple
        tail_x, tail_y = snake[-1]
        x_dir, y_dir = body_dir[-1]
        snake.append((tail_x - UNIT * x_dir, tail_y - UNIT * y_dir))
        body_dir.append((x_dir, y_dir))
        apple = random_apple()

    if not in_bounds(snake) or collision(snake):
        running = False
        break

    if not chain:
        chain_dir(body_dir)
    window.fill(black)
    move(snake, body_dir)
    draw(apple, snake)

    chain = False

    clock.tick(FPS)
    pygame.display.flip()


window.fill(red)
pygame.display.flip()
pygame.time.delay(1500)