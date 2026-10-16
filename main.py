import pygame
from os.path import join
from random import randint


# Sprite Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images',
                                            'player.png')).convert_alpha()
        self.rect = self.image.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )
        self.player_direction = pygame.math.Vector2((0, 0))
        self.player_speed = 400

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

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
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(all_sprites, surf=laser_surf, pos=self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, *groups, surf):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


class Laser(pygame.sprite.Sprite):
    def __init__(self, *groups, surf, pos,):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(
            midbottom=pos
        )

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


# Quick general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Plain surface
surf = pygame.Surface((100, 200))
surf.fill('blue')
x = 100

all_sprites = pygame.sprite.Group()

# star image
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for _ in range(20):
    Star(all_sprites, surf=star_surf)

# Spawn player
player = Player(all_sprites)

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)

# laser image
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()


# Custom events => meteor timer
event_meteor = pygame.event.custom_type()
pygame.time.set_timer(event_meteor, 1000)

# creating a single rect
# plain_rect = pygame.FRect(left, right, width, height)

# Flag for loop
running = True

# While loop
while running:
    # Frame rate
    dt = clock.tick(60) / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == event_meteor:
        #     print('Meteor Spawned...')

    all_sprites.update(dt)

    # Background
    display_surface.fill('darkgray')

    # displaying parts
    display_surface.blit(meteor_surf, meteor_rect)
    all_sprites.draw(display_surface)
    pygame.display.update()


pygame.quit()
