import pygame
from os.path import join
from random import randint


# quick general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# plain surface
surf = pygame.Surface((100, 200))
surf.fill('blue')
x = 100

# importing an image
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
# making a rectangle from player
player_rect = player_surf.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    )

# import star
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
# star positions
star_positions = [
    (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))for _ in range(20)
    ]

# flag for loop
running = True


# while loop
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill('darkgray')
    # placing 20 random stars with randint
    for pos in star_positions:
        display_surface.blit(star_surf, pos)

    # displaying player/animating
    if player_rect.right < WINDOW_WIDTH:
        player_rect.left += 0.2

    display_surface.blit(player_surf, player_rect)

    pygame.display.update()


pygame.quit()
