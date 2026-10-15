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
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    )
player_direction = pygame.math.Vector2(0, 0)
player_speed = 500

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
    dt = clock.tick(60) / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input
    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN] - int(keys[pygame.K_UP]))

    player_rect.center += player_direction * player_speed * dt
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
