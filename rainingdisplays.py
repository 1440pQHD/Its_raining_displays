import pygame
import random
import time

pygame.init()

font = pygame.font.SysFont(None, 36)
pause_font = pygame.font.SysFont(None, 64)


#options for the screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

#Options for the player

radius = 40
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

#Options for the target
target_x = random.randint(50, SCREEN_WIDTH - 50)
target_y = random.randint(50, SCREEN_HEIGHT - 50)
target_size = 20
score = 0

y_velocity = 0
gravity = 0.3
jump_strength = 11
is_jumping = False


#options for the screen shake
display_buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

shake_timer=0
shake_intensity= 0


def trigger_shake(duration_frames, intensity):
    global shake_timer, shake_intensity
    shake_timer = duration_frames
    shake_intensity = intensity

#pausing
paused = False

def shows_splash_screen():
    splash_duration = 3000
    start_time = pygame.time.get_ticks()

    waiting = True

    while waiting:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= splash_duration:
            waiting = False

        for event



while running:

    render_offset = [0, 0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                paused = not paused

    display_buffer.fill("purple")

    pygame.draw.circle(display_buffer, "red", player_pos, radius)

    if not paused:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not is_jumping and player_pos.y >= SCREEN_HEIGHT - radius - 1:
            y_velocity = -jump_strength
            is_jumping = True

        y_velocity += gravity
        player_pos.y += y_velocity

        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        if player_pos.x - radius < 0:
            player_pos.x = radius
        elif player_pos.x + radius > SCREEN_WIDTH:
            player_pos.x = SCREEN_WIDTH - radius

        if player_pos.y + radius >= SCREEN_HEIGHT:
            player_pos.y = SCREEN_HEIGHT - radius
            y_velocity = 0
            is_jumping = False
        elif player_pos.y - radius <= 0:
            player_pos.y = radius
            y_velocity = max(y_velocity, 0)

        player_rect = pygame.Rect(player_pos.x - radius, player_pos.y - radius, radius * 2, radius * 2)
        target_rect = pygame.Rect(target_x, target_y, target_size, target_size)

        if player_rect.colliderect(target_rect):
            shake_timer = 15
            shake_intensity = 5
            
            score += 1
            target_x = random.randint(50, SCREEN_WIDTH - 50)
            target_y = random.randint(50, SCREEN_HEIGHT - 50)

        if shake_timer > 0:
            render_offset[0] = random.randint(-shake_intensity, shake_intensity)
            render_offset[1] = random.randint(-shake_intensity, shake_intensity)
            shake_timer -= 1

        score_surface = font.render(f"Score: {score}", True, (0,0,0))

    score_surface = font.render(f"Score: {score}", True, (0, 0, 0))

    display_buffer.blit(score_surface, (20, 20))

    pygame.draw.rect(display_buffer, "red", (target_x, target_y, target_size, target_size))

    print(score)

    screen.blit(display_buffer, render_offset)

    if paused:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        pause_surface = pause_font.render("GAME PAUSED", True, (255, 255, 255))
        inst_surface = font.render("Press P or ESC to resume", True, (255, 255, 255))

        screen.blit(
            pause_surface,
            (
                SCREEN_WIDTH // 2 - pause_surface.get_width() // 2,
                SCREEN_HEIGHT // 2 - 50,
            ),
        )
        screen.blit(
            inst_surface,
            (
                SCREEN_WIDTH // 2 - inst_surface.get_width() // 2,
                SCREEN_HEIGHT // 2 + 10,
            ),
        )

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()




