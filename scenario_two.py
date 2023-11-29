import pygame
import sys
import os
import time

import random
import math

# Initialize Pygame
pygame.init()
display_info = pygame.display.Info()
# Constants
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CAR_WIDTH, CAR_HEIGHT = 70, 90
POTHOLE_WIDTH, POTHOLE_HEIGHT = 40, 40
LANE_WIDTH = WIDTH // 8
font = pygame.font.Font(None, 25)

RAIN_COLOR = (135, 206, 235)  # Light blue color for raindrops
# Raindrops list
raindrops = []
# Create the screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Change Scenario")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load images
car_img = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
car_img.fill(WHITE)

pothole_img = pygame.Surface((POTHOLE_WIDTH, POTHOLE_HEIGHT))
pothole_img.fill((255, 255, 255))

# Car properties
car_x = 30
car_y = HEIGHT - 3 * CAR_HEIGHT
car_speed = 0.5

car2_x = (20 * CAR_WIDTH) // 2.5
car2_y = HEIGHT - 1 * CAR_HEIGHT
car3_x = (20 * CAR_WIDTH) // 6.8
car3_y = HEIGHT - 1 * CAR_HEIGHT

# Pothole properties
pothole_x = 10
pothole_y = 20
pothole_speed = 1.5  # Increased pothole speed
pothole_timer = 300  # Introduce pothole 1 second earlier
car_lane = 0  # 0 for left lane, 1 for right lane
DIVIDER_COLOR = BLACK
final_position = car_x + LANE_WIDTH
message_loop = True

TRACK = pygame.image.load("road.png")
TRACK = pygame.transform.scale(TRACK, (WIDTH, HEIGHT))

# Load obstacle image
obstacle_image = pygame.image.load("obstacle.png")

# Create surface
combined_surface = pygame.Surface((TRACK.get_width(), TRACK.get_height()))

# Blit background onto surface
combined_surface.blit(TRACK, (0, 0))

# Get obstacle rectangle
obstacle_rect = obstacle_image.get_rect()

# Position obstacle on top of background
obstacle_rect.center = (300, 200)

# Blit obstacle onto surface

pygame.mixer.init()

# Load the background music
pygame.mixer.music.load(
    "rain_sound.mp3"
)  # Replace 'background_music.mp3' with your audio file

# Play the background music (-1 to loop indefinitely)
pygame.mixer.music.play(-1)


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(490, 820))
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []

    def update(self):
        self.radars.clear()
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
        self.data()

    def drive(self):
        self.rect.center += self.vel_vector * 6

    def collision(self):
        length = 40
        collision_point_right = [
            int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
            int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length),
        ]
        collision_point_left = [
            int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
            int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length),
        ]

        # Die on Collision
        if screen.get_at(collision_point_right) == pygame.Color(
            2, 105, 31, 255
        ) or screen.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
            self.alive = False

        # Draw Collision Points
        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_left, 4)

    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while (
            not screen.get_at((x, y)) == pygame.Color(2, 105, 31, 255) and length < 200
        ):
            length += 1
            x = int(
                self.rect.center[0]
                + math.cos(math.radians(self.angle + radar_angle)) * length
            )
            y = int(
                self.rect.center[1]
                - math.sin(math.radians(self.angle + radar_angle)) * length
            )

        # Draw Radar
        pygame.draw.line(screen, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(screen, (0, 255, 0, 0), (x, y), 3)

        dist = int(
            math.sqrt(
                math.pow(self.rect.center[0] - x, 2)
                + math.pow(self.rect.center[1] - y, 2)
            )
        )

        self.radars.append([radar_angle, dist])

    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Create new raindrops
    for i in range(10):  # Adjust the number of raindrops per frame
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        raindrops.append((x, y))

    # Move the raindrops
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        y += 5  # Adjust the speed of the raindrops falling
        raindrops[i] = (x, y)

        # Remove raindrops when they go below the screen
        if y > HEIGHT:
            raindrops[i] = (random.randint(0, WIDTH), random.randint(-HEIGHT, 0))

    # Draw the raindrops
    for x, y in raindrops:
        pygame.draw.line(
            screen, RAIN_COLOR, (x, y), (x, y + 2), 1
        )  # Adjust the line length and thickness

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)
    # Move the car

    car_y -= car_speed

    car2_y -= 1
    car3_y -= 0.3

    # Introduce ambulance after a certain time
    if pothole_timer > 0:
        pothole_timer -= 1
    else:
        pothole_y = pothole_speed

        # Check for shift condition
        if car_y < (7 * POTHOLE_HEIGHT) and car_lane == 0:
            while message_loop:
                message = font.render(
                    f"Pothole Ahead Switch Lane",
                    True,
                    (0, 0, 0),
                )
                screen.blit(message, (WIDTH // 1.8, 10))
                pygame.display.flip()
                time.sleep(2)
                message = font.render(
                    f"Car Red: Sure. Switching to lane 3.",
                    True,
                    (0, 0, 0),
                )
                screen.blit(message, (WIDTH // 1.8, 40))
                pygame.display.flip()
                time.sleep(2)
                message = font.render(f"Car Blue: Acknowledged.", True, (0, 0, 0))

                pygame.display.flip()
                time.sleep(2)
                message_loop = False

            car_lane = 0

            # car_x += LANE_WIDTH
            # car_y -= LANE_WIDTH

            car_x += 2 * car_speed
            car_y -= car_speed
            print("Car X = " + str(car_x) + " Car Y = " + str(car_y))
            if car_x >= final_position:
                car_lane = 2

    # Draw the background

    screen.fill(WHITE)
    pygame.draw.line(screen, DIVIDER_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    # combined_surface.blit(obstacle_image, obstacle_rect)

    # screen.blit(combined_surface, (0, 0))
    # Draw lanes
    # pygame.draw.line(screen, BLACK, (LANE_WIDTH, 0), (LANE_WIDTH, HEIGHT), 5)
    # pygame.draw.line(
    #     screen, WHITE, (WIDTH - LANE_WIDTH, 0), (WIDTH - LANE_WIDTH, HEIGHT), 5
    # )
    for i in range(1, 5):
        for j in range(0, HEIGHT, 10):
            pygame.draw.rect(screen, BLACK, (i * LANE_WIDTH, j, 2, 5))

    # Draw the ambulance
    pothole = pygame.image.load("obstacle.png")
    pothole = pygame.transform.scale(pothole, (POTHOLE_WIDTH * 3, POTHOLE_HEIGHT * 3))
    screen.blit(pothole, (pothole_x, pothole_y))

    # Draw the car
    car1 = pygame.sprite.GroupSingle(Car())
    car1 = pygame.image.load("car01.png")
    car1 = pygame.transform.scale(car1, (CAR_WIDTH * 2, CAR_HEIGHT * 2))

    screen.blit(car1, (car_x, car_y))

    car2 = pygame.image.load("car04.png")
    car2 = pygame.transform.scale(car2, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
    screen.blit(car2, (car2_x, car2_y))

    car3 = pygame.image.load("car06.png")
    car3 = pygame.transform.scale(car3, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
    screen.blit(car3, (car3_x, car3_y))
    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)
