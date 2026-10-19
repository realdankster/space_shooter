import pygame
from os.path import join
from random import randint, uniform


# Sprite Classes
class Player(pygame.sprite.Sprite):
    """The player-controlled spaceship."""

    def __init__(self, *groups):
        super().__init__(*groups)

        # Load the spaceship image and place it at the center of the window.
        self.image = pygame.image.load(
            join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Store the movement direction and movement speed.
        self.player_direction = pygame.math.Vector2((0, 0))
        self.player_speed = 400

        # Store the laser cooldown state and timing information.
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 1000

        # Create a pixel-perfect mask for collision detection.
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        """Allow the player to shoot again after the cooldown ends."""

        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        """Read player input, move the ship, and handle shooting."""

        # Read the current keyboard state and calculate the movement direction.
        keys = pygame.key.get_pressed()
        self.player_direction.x = int(
            keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]
                                        )

        self.player_direction.y = int(
            keys[pygame.K_DOWN] - int(keys[pygame.K_UP])
            )

        # Normalize diagonal movement so
        # it is not faster than horizontal or vertical movement.
        if self.player_direction.length() > 0:
            self.player_direction = self.player_direction.normalize()

        self.rect.center += self.player_direction * self.player_speed * dt

        # Create a laser when Space is newly pressed and the cooldown
        # has finished.
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites),
                  surf=laser_surf, pos=self.rect.midtop)
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()


class Star(pygame.sprite.Sprite):
    """A background star placed at a random position."""

    def __init__(self, *groups, surf):
        super().__init__(*groups)

        # Use the shared star image and place this star randomly in the window.
        self.image = surf
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


class Laser(pygame.sprite.Sprite):
    """A laser projectile fired by the player."""

    def __init__(self, *groups, surf, pos):
        super().__init__(*groups)

        # Use the laser image and position its bottom edge at the firing point.
        self.image = surf
        self.rect = self.image.get_frect(
            midbottom=pos
        )

        # Create a pixel-perfect mask for collision detection.
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        """Move the laser upward and remove it after it leaves the window."""

        # Move the laser upward and remove it when it passes the top boundary.
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    """A falling, rotating meteor that
    can collide with the player or a laser."""

    def __init__(self, *groups, surf, pos):
        super().__init__(*groups)

        # Store the original image so the meteor can be rotated
        # without compounding distortion.
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(
            center=pos
        )

        # Set the meteor's direction, movement speed, and rotation speed.
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(100, 300)
        self.rotation_speed = randint(100, 200)
        self.rotation = 0

        # Create a pixel-perfect mask for collision detection.
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        """Move and rotate the meteor, then remove it below the window."""

        # Move the meteor according to its direction, speed, and elapsed time.
        self.rect.center += self.direction * self.speed * dt

        # Remove the meteor after it moves below the bottom boundary.
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        # Rotate the meteor while keeping its center in the same position.
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(
            self.original_surf, self.rotation, 1
            )
        self.rect = self.image.get_frect(center=self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    """An explosion that displays a sequence of
    images and then removes itself."""

    def __init__(self, *groups, frames, pos):
        super().__init__(*groups)

        # Store the animation frames and begin with the first image.
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        """Advance the animation and remove the sprite
        after the final frame."""

        # Increase the frame position according to the elapsed time.
        self.frame_index += 50 * dt

        # Display the current frame, or remove the explosion
        # when the animation ends.
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


class Wasted(pygame.sprite.Sprite):
    def __init__(self, *groups,
                 window_width,
                 window_height,
                 font,
                 score):
        super().__init__(*groups)

        self.image = pygame.Surface(
            (window_width, window_height)
        )
        self.rect = self.image.get_frect(
            topleft=(0, 0)
        )
        self.image.fill('#632ea8')

        self.text_surface = font.render(
            f"You Died... Your Score Was: {score}",
            True,
            (200, 200, 200)
        )

        self.text_rect = self.text_surface.get_frect(
            center=(window_width / 2, window_height / 2)
        )

        self.image.blit(self.text_surface, self.text_rect)

        self.death_time = pygame.time.get_ticks()
        self.close_timer = 2000
        self.finished = False

    def update(self, dt):
        current_time = pygame.time.get_ticks()

        if current_time - self.death_time >= self.close_timer:
            self.finished = True


# Flag for wasted screen
wasted_screen = None


def collision(wasted_screen):
    """Handle laser-meteor collisions and player-meteor collisions."""

    # Access the game-loop flag so a meteor collision can end the game.
    global running

    # Track Score
    score = pygame.time.get_ticks() // 1000

    # Check every laser for a pixel-perfect collision with a meteor.
    for laser in laser_sprites:
        collision = pygame.sprite.spritecollide(
            laser, meteor_sprites, True, pygame.sprite.collide_mask
            )
        if collision:
            laser.kill()
            # Create and play an explosion at the laser's collision position.
            AnimatedExplosion(
                all_sprites, frames=explosion_frames, pos=laser.rect.midtop
            )
            explosion_sound.play()
    collision_sprites = pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    )

    # End the game when a meteor collides with the player.
    if collision_sprites and wasted_screen is None:
        wasted_screen = Wasted(
            all_sprites,
            window_width=WINDOW_WIDTH,
            window_height=WINDOW_HEIGHT,
            font=font,
            score=score
        )
        game_sound.stop()
        gameover_sound.play()

    return wasted_screen


def display_score():
    """Display the number of seconds that have elapsed during the game."""

    # Convert the elapsed time from milliseconds to whole seconds.
    current_time = pygame.time.get_ticks() // 1000

    # Render the elapsed time as text.
    text_surf = font.render(str(current_time), True, (220, 220, 220))

    # Position the score near the bottom center of the window.
    text_rect = text_surf.get_frect(
        midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30)
    )

    # Draw the score text to the display surface.
    display_surface.blit(text_surf, text_rect)

    # Draw a rounded border around the score.
    pygame.draw.rect(
        display_surface, (220, 220, 220),
        text_rect.inflate(20, 5).move(0, -6), 5, 5
        )


def update_game(dt, wasted_screen, running):
    display_surface.fill('#392640')

    if wasted_screen is None:
        # Normal game
        all_sprites.update(dt)

        wasted_screen = collision(wasted_screen)

        display_score()
        all_sprites.draw(display_surface)

    else:
        # Wasted screen
        all_sprites.update(dt)
        all_sprites.draw(display_surface)
        if wasted_screen.finished:
            running = False

    return wasted_screen, running


# Initialize Pygame and prepare the game.
pygame.init()

# Set the game window dimensions.
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# Create the display surface used to draw the game.
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Create a clock to measure elapsed time between frames.
clock = pygame.time.Clock()

# Create sprite groups for all sprites and for collision-related sprites.
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# Load the font used by the score display.
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)

# Load every image used by the explosion animation.
explosion_frames = [pygame.image.load(join(
    'images', 'explosion', f'{i}.png'
)).convert_alpha() for i in range(21)]

# Load the game's sound effects and background music.
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_sound = pygame.mixer.Sound(join('audio', 'game_music.wav'))
gameover_sound = pygame.mixer.Sound(join('audio', 'GameOver.wav'))

# Set the volume for each sound.
laser_sound.set_volume(0.4)
explosion_sound.set_volume(0.5)
game_sound.set_volume(0.1)
gameover_sound.set_volume(0.4)

# Start the background music and loop it continuously.
game_sound.play(loops=-1)

# Load the images used by the stars, meteors, and lasers.
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
for _ in range(20):
    Star(all_sprites, surf=star_surf)

# Create the player sprite and add it to the main sprite group.
player = Player(all_sprites)

# Create a custom event that periodically spawns a new meteor.
event_meteor = pygame.event.custom_type()
pygame.time.set_timer(event_meteor, 600)

# Keep the main game loop running until the player quits or loses.
running = True

while running:
    """Main game loop: process events, update sprites,
    detect collisions, and draw."""

    # Calculate elapsed time in seconds for frame-rate-independent movement.
    dt = clock.tick(120) / 1000

    # Process window events and periodically create new meteors.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == event_meteor and wasted_screen is None:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), surf=meteor_surf, pos=(x, y))

    wasted_screen, running = update_game(
        dt,
        wasted_screen,
        running
    )

    pygame.display.update()

pygame.quit()
