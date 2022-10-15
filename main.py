import pygame

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 810
BACKGROUND_COLOR = (24, 24, 24)

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

is_active = True
while is_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_active = False
    screen.fill(BACKGROUND_COLOR)
    pygame.display.update()

pygame.quit()