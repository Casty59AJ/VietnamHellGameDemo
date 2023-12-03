import pygame
from pygame import mixer
import random
import time

pygame.init()
mixer.init()

WIDTH = 1050
HEIGHT = 700
BORDER_THICKNESS = 1

BACKGROUND = pygame.Color(255, 255, 255)
WALLS = pygame.Color(0, 0, 0)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game for David")

hit_snd = pygame.mixer.Sound('snd/death_snd.mp3')
shoot_snd = pygame.mixer.Sound('snd/shoot.wav') # load it for now, use later

# squares 'n shit

class PlayerCube():
    def __init__(self):
        cube_img = pygame.image.load('img/player_cube.png')  # load player sprite
        self.cube_image = pygame.transform.scale(cube_img, (32, 32))
        self.rect = self.cube_image.get_rect()
        self.rect.x = (WIDTH - self.rect.width) // 2
        self.rect.y = HEIGHT - 128
        self.hit = False

    def update(self, enemy_rect, walls):
        key = pygame.key.get_pressed()

        new_x = self.rect.x
        new_y = self.rect.y

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            new_x -= 1
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            new_x += 1
        if key[pygame.K_w] or key[pygame.K_UP]:
            new_y -= 1
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            new_y += 1

        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall):
                if new_x < self.rect.x:  # moving left
                    new_x = wall.x + wall.width
                elif new_x > self.rect.x:  # moving right
                    new_x = wall.x - self.rect.width
                if new_y < self.rect.y:  # moving up
                    new_y = wall.y + wall.height
                elif new_y > self.rect.y:  # moving down
                    new_y = wall.y - self.rect.height

        if BORDER_THICKNESS <= new_x <= WIDTH - BORDER_THICKNESS - self.rect.width:
            self.rect.x = new_x
        if BORDER_THICKNESS <= new_y <= HEIGHT - BORDER_THICKNESS - self.rect.height:
            self.rect.y = new_y

        if self.rect.colliderect(enemy_rect):
            self.hit = True
            hit_snd.play()

        window.blit(self.cube_image, self.rect)

class EnemyCube():
    def __init__(self):
        cube_img = pygame.image.load('img/enemy_cube.png')
        self.cube_image = pygame.transform.scale(cube_img, (32, 32))
        self.rect = self.cube_image.get_rect()
        self.rect.x = random.randint(BORDER_THICKNESS, WIDTH - BORDER_THICKNESS - self.rect.width)
        self.rect.y = random.randint(BORDER_THICKNESS, HEIGHT - BORDER_THICKNESS - self.rect.height)
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self, walls):
        if self.direction == "left" and self.rect.x > BORDER_THICKNESS:
            self.rect.x -= 1
        elif self.direction == "right" and self.rect.x < WIDTH - BORDER_THICKNESS - self.rect.width:
            self.rect.x += 1
        elif self.direction == "up" and self.rect.y > BORDER_THICKNESS:
            self.rect.y -= 1
        elif self.direction == "down" and self.rect.y < HEIGHT - BORDER_THICKNESS - self.rect.height:
            self.rect.y += 1
        else:
            # Change direction if hitting a border
            self.direction = random.choice(["left", "right", "up", "down"])

        window.blit(self.cube_image, self.rect)

# Define the maze with walls
walls = [
    pygame.Rect(100, 100, 200, 20),
    pygame.Rect(300, 200, 20, 150),
    pygame.Rect(500, 100, 200, 20),
    # Add more walls as needed
]

player_cube = PlayerCube()
enemy_cube = EnemyCube()

running = True
while running and not player_cube.hit:

    window.fill(BACKGROUND)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(window, WALLS, wall)

    player_cube.update(enemy_cube.rect, walls)
    enemy_cube.update(walls)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

time.sleep(2)
pygame.quit()