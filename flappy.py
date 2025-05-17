import pygame
import random
import sys

# Initialize
pygame.init()


# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Load bird image
bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (60, 50))  # width=40, height=30

# Bird setup
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 20
gravity = 0.5
velocity = 0
jump_strength = -10

# Pipe setup
pipe_width = 70
pipe_gap = 200
pipe_x = WIDTH
pipe_height = random.randint(100, 400)

# Speed setup
pipe_speed = 3         # Initial pipe speed
speed_increase = 0.002 # Amount to increase each frame

# Score
score = 0
game_over = False

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

# Main game loop
while True:
    screen.fill((135, 206, 235))  # Sky blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = jump_strength

    if not game_over:
        # Gravity and bird movement
        velocity += gravity
        bird_y += velocity

        # Move pipes
        pipe_x -= pipe_speed

        # Increase pipe speed gradually
        pipe_speed += speed_increase

        # Reset pipe if it goes off screen
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            score += 1  # Increase score when pipe resets

        # Draw pipes
        top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)
        pygame.draw.rect(screen, (0, 255, 0), top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), bottom_pipe)

        # Draw bird
        bird_rect = pygame.Rect(bird_x - bird_img.get_width() // 2, bird_y - bird_img.get_height() // 2, bird_img.get_width(), bird_img.get_height())
        # Draw bird (image)
        screen.blit(bird_img, (bird_x - bird_img.get_width() // 2, int(bird_y) - bird_img.get_height() // 2))


        # Check collision
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe) or bird_y > HEIGHT or bird_y < 0:
            game_over = True

        # Display score
        draw_text(f"Score: {score}", 36, (255, 255, 255), WIDTH // 2, 40)

    else:
        draw_text("Game Over!", 64, (255, 0, 0), WIDTH // 2, HEIGHT // 2)
        draw_text(f"Final Score: {score}", 48, (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 60)
        draw_text("Press R to Restart", 32, (200, 200, 200), WIDTH // 2, HEIGHT // 2 + 120)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            bird_y = HEIGHT // 2
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            velocity = 0
            score = 0
            game_over = False
            pipe_speed = 3  # Reset speed

    pygame.display.flip()
    clock.tick(60)