import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CAR_WIDTH, CAR_HEIGHT = 50, 30
AMBULANCE_WIDTH, AMBULANCE_HEIGHT = 50, 30
LANE_WIDTH = 100

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Change Scenario")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load images
car_img = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
car_img.fill(WHITE)

ambulance_img = pygame.Surface((AMBULANCE_WIDTH, AMBULANCE_HEIGHT))
ambulance_img.fill((255, 0, 0))

# Car properties
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - 2 * CAR_HEIGHT
car_speed = 5

# Ambulance properties
ambulance_x = WIDTH // 2 - AMBULANCE_WIDTH // 2
ambulance_y = HEIGHT + 20
ambulance_speed = 10  # Increased ambulance speed
ambulance_timer = FPS  # Introduce ambulance 1 second earlier
car_lane = 0  # 0 for left lane, 1 for right lane

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the car
    car_y -= car_speed

    # Introduce ambulance after a certain time
    if ambulance_timer > 0:
        ambulance_timer -= 1
    else:
        ambulance_y -= ambulance_speed

        # Check for shift condition
        if ambulance_y < HEIGHT - AMBULANCE_HEIGHT and car_lane == 0:
            car_lane = 1
            car_x += LANE_WIDTH

    # Draw the background
    screen.fill(BLACK)

    # Draw lanes
    pygame.draw.line(screen, WHITE, (LANE_WIDTH, 0), (LANE_WIDTH, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (WIDTH - LANE_WIDTH, 0),
                     (WIDTH - LANE_WIDTH, HEIGHT), 5)

    # Draw the ambulance
    screen.blit(ambulance_img, (ambulance_x, ambulance_y))

    # Draw the car
    screen.blit(car_img, (car_x, car_y))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
