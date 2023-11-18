import unittest
import pygame
import sys
import random

WIDTH, HEIGHT = 800, 600
FPS = 60

HOME_SCREEN = "home"
GAME_SCREEN = "game"
GAME_OVER_SCREEN = "game_over"
obstacle_count = 2

class TestSpaceInvaders(unittest.TestCase):
    def setUp(self):
        # Initialize any required setup before each test
        pygame.init()
        pygame.key.set_mods(0)  # Reset key mods

    def tearDown(self):
        # Clean up any resources after each test
        pygame.quit()

    def reset_global_state(self):
        global game_state, player_x, player_y, player_score, obstacle_speeds, obstacles
        game_state = HOME_SCREEN
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

    def test_player_movement(self):
        self.reset_global_state()
        global player_speed, player_x
        player_speed = 8
        player_x = WIDTH // 2
        global player_y
        player_y = HEIGHT - 50

        # Test moving left
        keys = list(pygame.key.get_pressed())
        keys[pygame.K_LEFT] = True
        pygame.key.set_mods(keys)
        player_movement()
        self.assertEqual(player_x, WIDTH // 2 - player_speed)

       # Test moving right
        keys[pygame.K_RIGHT] = True
        player_movement()
        self.assertEqual(player_x, WIDTH // 2 + player_speed)

        # Test not moving beyond screen boundaries
        player_x = WIDTH - 60
        keys[pygame.K_RIGHT] = True
        pygame.key.set_mods(keys)
        player_movement()
        self.assertEqual(player_x, WIDTH - 50)

        # Test not moving beyond screen boundaries
        player_x = WIDTH - 60
        keys[pygame.K_RIGHT] = True
        pygame.key.set_mods(keys)
        player_movement()
        self.assertEqual(player_x, WIDTH - 50)

    def test_shooting_functionality(self):
        self.reset_global_state()
        global player_bullet_state, player_bullet_x, player_bullet_y
        player_bullet_state = "ready"
        player_bullet_x = 0
        player_bullet_y = HEIGHT - 50

        # Test shooting
        keys = list(pygame.key.get_pressed())
        keys[pygame.K_SPACE] = True
        shooting_functionality()
        self.assertEqual(player_bullet_state, "fire")
        self.assertEqual(player_bullet_x, WIDTH // 2 + 25)
        self.assertEqual(player_bullet_y, HEIGHT - 50)

        # Test bullet moving upward
        player_bullet_state = "fire"
        shooting_functionality()
        self.assertEqual(player_bullet_y, HEIGHT - 60)

        # Test bullet state changing to "ready" at the top
        player_bullet_y = 0
        shooting_functionality()
        self.assertEqual(player_bullet_state, "ready")


    def test_obstacle_movement(self):
        self.reset_global_state()
        global obstacle_speeds
        player_score = 20
        obstacle_speeds = [2, 2, 2]
        obstacle = [WIDTH // 2, 0, "active", 0]

        # Test obstacle moving downward
        obstacle_movement(obstacle, player_score, obstacle_speeds)
        self.assertEqual(obstacle[1], 2)

        # Test obstacle respawning at random position
        obstacle[1] = HEIGHT
        obstacle_movement(obstacle, player_score, obstacle_speeds)
        self.assertEqual(obstacle[1], 0)
        self.assertTrue(obstacle[0] >= 0 and obstacle[0] <= WIDTH - 50)

        # Test obstacle speed increasing
        obstacle_movement(obstacle, player_score, obstacle_speeds)
        self.assertEqual(obstacle_speeds[0], 3)

    def test_collision_detection(self):
        self.reset_global_state()
        global player_bullet_state, player_bullet_x, player_bullet_y, player_score, obstacles, game_state
        player_bullet_state = "fire"
        player_bullet_x = WIDTH // 2
        player_bullet_y = HEIGHT // 2
        player_score = 0
        game_state = GAME_SCREEN
        obstacles = [[WIDTH // 2, HEIGHT // 2, "active", 0]]

        # Test player's score increasing
        collision_detection(obstacles[0])
        self.assertEqual(player_score, 1)

        # Test obstacle resetting when hit by a bullet
        self.assertEqual(obstacles[0][2], "ready")

        # Test game state changing to "GAME_OVER_SCREEN" when player collides with an obstacle
        player_x = WIDTH // 2
        player_y = HEIGHT // 2
        obstacles[0] = [player_x, player_y, "active", 0]
        collision_detection(obstacles[0])
        self.assertEqual(game_state, GAME_OVER_SCREEN)
        
    def test_game_over_and_restart(self):
        self.reset_global_state()
        global game_state, player_x, player_y, player_score, obstacle_speeds, obstacles
        game_state = GAME_OVER_SCREEN
        player_x = WIDTH // 2
        player_y = HEIGHT // 2
        player_score = 10
        obstacle_speeds = [2, 3, 4]
        obstacles = []

        # Test game restarting
        keys = pygame.key.get_pressed()
        keys[pygame.K_SPACE] = True
        game_over_and_restart()
        self.assertEqual(game_state, GAME_SCREEN)
        self.assertEqual(player_x, WIDTH // 2)
        self.assertEqual(player_y, HEIGHT - 50)
        self.assertEqual(player_score, 0)
        self.assertEqual(obstacle_speeds, [2, 3, 4])
        self.assertEqual(len(obstacles), 2)  # assuming obstacle_count is 2

if __name__ == '__main__':
    unittest.main()
