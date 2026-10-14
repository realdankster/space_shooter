import pygame

# quick general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# flag for loop
running = True

# while loop
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
pygame.quit()
