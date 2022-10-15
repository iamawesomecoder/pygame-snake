import pygame
from random import randrange
from time import sleep

### Config Constants ###
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 800
FPS = 20
### **************** ###

### Color Constants ###
DARK_GREY = (24, 24, 24)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 255)
### *************** ###

### Other Game Constants ###
SCORE_INCREMENT_AMOUNT = 10
### ******************** ###

### Game Object Constants ###
SQUARE_SIZE = 20
### ********************* ###

### Direction Enum ###
DIRECTION_LEFT = 0
DIRECTION_RIGHT = 1
DIRECTION_UP = 2
DIRECTION_DOWN = 3
DIRECTION_SAME = 4
### ************** ###

### Global Function Definitations ###
def randomized_food_position():
    x = randrange(1, (WINDOW_WIDTH // SQUARE_SIZE)) * SQUARE_SIZE
    y = randrange(1, (WINDOW_HEIGHT // SQUARE_SIZE)) * SQUARE_SIZE
    return (x, y)

def get_starting_segments_for_snake():
    return [
        list(snake_head_position), 
        [snake_head_position[0] - SQUARE_SIZE, snake_head_position[1]],
        [snake_head_position[0] - SQUARE_SIZE * 2, snake_head_position[1]]
    ]

def handle_snake_movement():
    global snake_head_position, snake_direction_change_to, snake_direction, score, food_position

    # Whether snake's direction needs to be changed; if so then change the direction.
    if snake_direction_change_to != DIRECTION_SAME:
        if snake_direction_change_to == DIRECTION_LEFT and snake_direction != DIRECTION_RIGHT:
            snake_direction = DIRECTION_LEFT
        elif snake_direction_change_to == DIRECTION_RIGHT and snake_direction != DIRECTION_LEFT:
            snake_direction = DIRECTION_RIGHT
        elif snake_direction_change_to == DIRECTION_UP and snake_direction != DIRECTION_DOWN:
            snake_direction = DIRECTION_UP
        elif snake_direction_change_to == DIRECTION_DOWN and snake_direction != DIRECTION_UP:
            snake_direction = DIRECTION_DOWN

        snake_direction_change_to = DIRECTION_SAME

    # Move the snake in current direction.
    if snake_direction == DIRECTION_LEFT:
        snake_head_position[0] -= SQUARE_SIZE
    elif snake_direction == DIRECTION_RIGHT:
        snake_head_position[0] += SQUARE_SIZE
    elif snake_direction == DIRECTION_UP:
        snake_head_position[1] -= SQUARE_SIZE
    elif snake_direction == DIRECTION_DOWN:
        snake_head_position[1] += SQUARE_SIZE

    # Snake growing logic.
    snake_segment_positions.insert(0, list(snake_head_position))
    if snake_collides_with(food_position):
        score += SCORE_INCREMENT_AMOUNT
        food_position = randomized_food_position()
    else:
        snake_segment_positions.pop()

def snake_collides_with(position):
    return snake_head_position[0] == position[0] and snake_head_position[1] == position[1]

def handle_game_over():
    # When snake hits the walls.
    if snake_head_position[0] < 0 or snake_head_position[0] > WINDOW_WIDTH - SQUARE_SIZE:
        return game_over()
    if snake_head_position[1] < 0 or snake_head_position[1] > WINDOW_HEIGHT - SQUARE_SIZE:
        return game_over()
    
    # When snake hits its own body.
    for segment_position in snake_segment_positions[1:]:
        if snake_collides_with(segment_position):
            return game_over()

def draw_score():
    score_surface = SCORE_FONT.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (WINDOW_HEIGHT / 10, 30)
    screen.blit(score_surface, score_rect)

def game_over():
    global score, food_position, snake_head_position, snake_segment_positions, snake_direction_change_to, snake_direction

    sleep(3)
    food_position = randomized_food_position()
    score = 0
    snake_head_position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
    snake_segment_positions = get_starting_segments_for_snake()
    snake_direction = DIRECTION_RIGHT
    snake_direction_change_to = DIRECTION_SAME
### ***************************** ###


pygame.init()

# Create the window.
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

fps_controller = pygame.time.Clock()

score = 0
SCORE_FONT = pygame.font.SysFont('consolas', 24)

# Initialize the snake.
snake_direction = DIRECTION_RIGHT
snake_direction_change_to = DIRECTION_SAME
snake_head_position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
snake_segment_positions = get_starting_segments_for_snake()

# Initialize the food.
food_position = randomized_food_position()

# Main game loop.
is_active = True
while is_active:
    # Check for events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake_direction_change_to = DIRECTION_LEFT
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake_direction_change_to = DIRECTION_RIGHT
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake_direction_change_to = DIRECTION_UP
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake_direction_change_to = DIRECTION_DOWN

    handle_snake_movement()
    handle_game_over()

    # Draw the background.
    screen.fill(DARK_GREY)

    # Draw the food.
    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], SQUARE_SIZE, SQUARE_SIZE))

    # Draw the snake.
    for position in snake_segment_positions:
        pygame.draw.rect(screen, GREEN, (position[0], position[1], SQUARE_SIZE, SQUARE_SIZE))

    draw_score()

    # Update the window.
    pygame.display.update()

    fps_controller.tick(FPS)

pygame.quit()