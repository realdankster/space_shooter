import pygame
from os.path import join
from random import randint


# quick general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100, 200))
surf.fill('blue')
x = 100

# imports/rects
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(
    midleft=(0, WINDOW_HEIGHT / 2)
    )
player_direction = pygame.math.Vector2(5, -3)
player_speed = 20

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)


laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(
    bottomleft=(20, WINDOW_HEIGHT - 20)
)


star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [
    (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))for _ in range(20)
    ]


# creating a single rect
# plain_rect = pygame.FRect(left, right, width, height)

# flag for loop
running = True


# while loop
while running:
    # frame rate
    dt = clock.tick(120) / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("1")
        if event.type == pygame.MOUSEMOTION:
            player_rect.center = event.pos

    # draw the game
    display_surface.fill('darkgray')
    # placing 20 random stars with randint
    for pos in star_positions:
        display_surface.blit(star_surf, pos)

    # displaying player/animating
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()


pygame.quit()
