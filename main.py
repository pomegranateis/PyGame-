import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load player image with transparent background
player_img = pygame.image.load("6206454607187545408.webp").convert_alpha()
player_img = pygame.transform.scale(player_img, (65, 65))

# Load obstacle images with transparent backgrounds
obstacle_imgs = [
    pygame.image.load("6206454607187545401.webp").convert_alpha(),
    pygame.image.load("6206454607187545402.webp").convert_alpha(),
    pygame.image.load("6206454607187545404.webp").convert_alpha(),
]

for i in range(3):
    obstacle_imgs[i] = pygame.transform.scale(obstacle_imgs[i], (50, 50))

# Create fonts for home and game screens with different colors
font = pygame.font.Font("Super Milk.ttf", 48)  # Default font
home_font = pygame.font.Font("Minecrafter.Reg.ttf", 72)  # Custom font with transparent background

# Define font colors
font_color_default = (255, 192, 203)
font_color_home = (255, 192, 203)
font_color_game = (255, 192, 203)
font_color_game_over = (255, 192, 203)

# Load sound effects
shoot_sound = pygame.mixer.Sound("shoot.mp3")
explosion_sound = pygame.mixer.Sound("explosion.mp3")

# Game states
HOME_SCREEN = "home"
GAME_SCREEN = "game"
GAME_OVER_SCREEN = "game_over"
game_state = HOME_SCREEN

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_speed = 8  # Increase player's movement speed
player_bullet_x = 0
player_bullet_y = player_y
player_bullet_state = "ready"
player_score = 0

obstacle_count = 2  # Fewer obstacles
obstacles = []
obstacle_speeds = [2, 2, 2]  # Speeds for three obstacle types

# Create obstacle objects
for _ in range(obstacle_count):
    obstacle_x = random.randint(0, WIDTH - 50)
    obstacle_y = random.randint(50, 150)
    obstacle_type = random.randint(0, 2)  # Randomly choose an obstacle type
    obstacles.append([obstacle_x, obstacle_y, "active", obstacle_type])

# Load background images for home and game screens with transparent backgrounds
home_screen_background = pygame.image.load("game_background.jpg").convert_alpha()
home_screen_background = pygame.transform.scale(home_screen_background, (WIDTH, HEIGHT))

game_screen_background = pygame.image.load("game_background.jpg").convert_alpha()
game_screen_background = pygame.transform.scale(game_screen_background, (WIDTH, HEIGHT))

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == HOME_SCREEN:
        # Home Screen
        screen.blit(home_screen_background, (0, 0))  # Set the home screen background image
        text = home_font.render("Space Invaders", True, font_color_home)  # Larger font with red color
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))  # Adjusted position
        screen.blit(text, text_rect)

        start_text = font.render("Press Space to Start", True, font_color_default)  # Default font with black color
        start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(start_text, start_text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = GAME_SCREEN

    elif game_state == GAME_SCREEN:
        # Main Game Screen
        screen.blit(game_screen_background, (0, 0))  # Set the game screen background image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed

        # Shooting functionality
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if player_bullet_state == "ready":
                player_bullet_x = player_x + 25
                player_bullet_y = player_y
                player_bullet_state = "fire"
                shoot_sound.play()  # Play the shooting sound

        # Player
        screen.blit(player_img, (player_x, player_y))

        # Player Bullet
        if player_bullet_state == "fire":
            pygame.draw.rect(screen, (0, 255, 0), (player_bullet_x, player_bullet_y, 2, 10))
            player_bullet_y -= 10
            if player_bullet_y <= 0:
                player_bullet_state = "ready"

        # Obstacles
        for i, obstacle in enumerate(obstacles):
            if obstacle[2] == "active":
                screen.blit(obstacle_imgs[obstacle[3]], (obstacle[0], obstacle[1]))
                obstacle[1] += obstacle_speeds[obstacle[3]]
                if obstacle[1] >= HEIGHT:
                    obstacle_x = random.randint(0, WIDTH - 50)
                    obstacle_y = random.randint(50, 150)
                    obstacle_type = random.randint(0, 2)
                    obstacles[i] = [obstacle_x, obstacle_y, "active", obstacle_type]

                # Collision detection
                if (
                    player_bullet_x >= obstacle[0]
                    and player_bullet_x <= obstacle[0] + 50
                    and player_bullet_y >= obstacle[1]
                    and player_bullet_y <= obstacle[1] + 50
                ):
                    player_bullet_state = "ready"
                    obstacle_x = random.randint(0, WIDTH - 50)
                    obstacle_y = random.randint(50, 150)
                    obstacle_type = random.randint(0, 2)
                    obstacles[i] = [obstacle_x, obstacle_y, "active", obstacle_type]
                    player_score += 1
                    explosion_sound.play()  # Play the explosion sound

                # Player collision with obstacles
                if (
                    player_x + 50 >= obstacle[0]
                    and player_x <= obstacle[0] + 50
                    and player_y + 50 >= obstacle[1]
                    and player_y <= obstacle[1] + 50
                ):
                    game_state = GAME_OVER_SCREEN

        # Display Score on the main game screen
        score_text = font.render("Score: " + str(player_score), True, font_color_game)  # Default font with blue color
        screen.blit(score_text, (10, 10))

        # Increase obstacle speed over time
        for i, speed in enumerate(obstacle_speeds):
            if player_score >= 10 * (i + 1):
                obstacle_speeds[i] += 1

    elif game_state == GAME_OVER_SCREEN:
        # Game Over Screen
        screen.blit(home_screen_background, (0, 0))  # Set the home screen background image
        game_over_text = home_font.render("Game Over", True, font_color_game_over)  # Larger font with red color
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))  # Adjusted position
        screen.blit(game_over_text, game_over_text_rect)

        score_text = font.render("Score: " + str(player_score), True, font_color_game)  # Default font with blue color
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(score_text, score_text_rect)

        restart_text = font.render("Press Space to Restart", True, font_color_default)  # Default font with black color
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = GAME_SCREEN
            player_x = WIDTH // 2
            player_y = HEIGHT - 50
            player_score = 0
            obstacle_speeds = [2, 3, 4]
            obstacles = []
            for _ in range(obstacle_count):
                obstacle_x = random.randint(0, WIDTH - 50)
                obstacle_y = random.randint(50, 150)
                obstacle_type = random.randint(0, 2)
                obstacles.append([obstacle_x, obstacle_y, "active", obstacle_type])

    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
