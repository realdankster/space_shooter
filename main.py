import pygame
from os.path import join
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images',
                                            'player.png')).convert_alpha()
        self.rect = self.image.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )
        self.player_direction = pygame.math.Vector2((0, 0))
        self.player_speed = 800

    def update(self, dt):
        # input
        keys = pygame.key.get_pressed()
        self.player_direction.x = int(
            keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]
                                        )

        self.player_direction.y = int(
            keys[pygame.K_DOWN] - int(keys[pygame.K_UP])
            )

        if self.player_direction.length() > 0:
            self.player_direction = self.player_direction.normalize()

        self.rect.center += self.player_direction * self.player_speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("laser fire")


class Star(pygame.sprite.Sprite):
    def __init__(self, *groups, surf):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


# quick general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100, 200))
surf.fill('blue')
x = 100

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
player = Player(all_sprites)
for _ in range(20):
    Star(all_sprites, surf=star_surf)

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)


laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(
    bottomleft=(20, WINDOW_HEIGHT - 20)
)


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

    all_sprites.update(dt)

    # draw the game
    display_surface.fill('darkgray')
    # placing 20 random stars with randint

    # displaying player/animating
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(meteor_surf, meteor_rect)
    all_sprites.draw(display_surface)
    pygame.display.update()


pygame.quit()
