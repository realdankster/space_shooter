import pygame
from os.path import join
from random import randint, uniform


# Sprite Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(
            join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )
        self.player_direction = pygame.math.Vector2((0, 0))
        self.player_speed = 400

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500

        # mask
        self.mask = pygame.mask.from_surface(self.image)
        # mask_surf = mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))
        # self.image = mask_surf

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
            Laser((all_sprites, laser_sprites),
                  surf=laser_surf, pos=self.rect.midtop)
            laser_sound.play()
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
    def __init__(self, *groups, surf, pos):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(
            midbottom=pos
        )
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, *groups, surf, pos):
        super().__init__(*groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(
            center=pos
        )
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(100, 300)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_speed = randint(100, 200)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(
            self.original_surf, self.rotation, 1
            )
        self.rect = self.image.get_frect(center=self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, *groups, frames, pos):
        super().__init__(*groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 50 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


def collision():

    global running

    for laser in laser_sprites:
        collision = pygame.sprite.spritecollide(
            laser, meteor_sprites, True, pygame.sprite.collide_mask
            )
        if collision:
            laser.kill()
            AnimatedExplosion(
                all_sprites, frames=explosion_frames, pos=laser.rect.midtop
            )
            explosion_sound.play()
    collision_sprites = pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    )
    if collision_sprites:
        running = False


def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, (220, 220, 220))
    text_rect = text_surf.get_frect(
        midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30)
    )
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(
        display_surface, (220, 220, 220),
        text_rect.inflate(20, 5).move(0, -6), 5, 5
        )


# Quick general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join(
    'images', 'explosion', f'{i}.png'
)).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.5)
game_sound = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_sound.set_volume(0.1)
game_sound.play(loops=-1)

# star image
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for _ in range(20):
    Star(all_sprites, surf=star_surf)

# Spawn player
player = Player(all_sprites)

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()

# laser image
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()

# Custom events => meteor timer
event_meteor = pygame.event.custom_type()
pygame.time.set_timer(event_meteor, 600)

# Flag for loop
running = True

# While loop
while running:
    # Frame rate
    dt = clock.tick(120) / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == event_meteor:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), surf=meteor_surf, pos=(x, y))

    all_sprites.update(dt)

    # Background
    display_surface.fill('#392640')

    # collision test
    collision()

    # displaying parts
    display_score()
    all_sprites.draw(display_surface)
    pygame.display.update()


pygame.quit()
