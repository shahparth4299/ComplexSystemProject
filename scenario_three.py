import pygame
import sys
import os
import time


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
AMBULANCE_WIDTH, AMBULANCE_HEIGHT = 70, 90
LANE_WIDTH = WIDTH // 8
font = pygame.font.Font(None, 25)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Change Scenario")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load images
car_img = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
car_img.fill(BLACK)

ambulance_img = pygame.Surface((AMBULANCE_WIDTH, AMBULANCE_HEIGHT))
ambulance_img.fill((255, 0, 0))

# Car properties
car_x = 30
car_y = HEIGHT - 3 * CAR_HEIGHT
car_speed = 0.5

car2_x = (WIDTH - CAR_WIDTH) // 2.5
car2_y = HEIGHT - 1 * CAR_HEIGHT
car3_x = (WIDTH - CAR_WIDTH) // 6.8
car3_y = HEIGHT - 1 * CAR_HEIGHT

# Ambulance properties
ambulance_x = 10
ambulance_y = HEIGHT + 20
ambulance_speed = 1.5  # Increased ambulance speed
ambulance_timer = 300  # Introduce ambulance 1 second earlier
car_lane = 0  # 0 for left lane, 1 for right lane
DIVIDER_COLOR = BLACK
final_position = car_x + LANE_WIDTH
message_loop = True
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the car

    car_y -= car_speed

    car2_y -= 1
    car3_y -= 0.3

    # Introduce ambulance after a certain time
    if ambulance_timer > 0:
        ambulance_timer -= 1
    else:
        ambulance_y -= ambulance_speed

        # Check for shift condition
        if ambulance_y < HEIGHT - AMBULANCE_HEIGHT and car_lane == 0:
            while message_loop:
                message = font.render(
                    f"Ambulance: Please clear the lane 4. Ambulance incoming",
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

                screen.blit(message, (WIDTH // 1.8, 70))
                pygame.display.flip()
                time.sleep(2)
                message = font.render(
                    f"Ambulance: Acknowledged. Passing through.", True, (0, 0, 0)
                )

                screen.blit(message, (WIDTH // 1.8, 100))
                pygame.display.flip()
                time.sleep(2)
                message_loop = False

            car_lane = 0

            # car_x += LANE_WIDTH
            # car_y -= LANE_WIDTH

            car_x += car_speed
            car_y -= car_speed
            print("Car X = " + str(car_x) + " Car Y = " + str(car_y))
            if car_x >= final_position:
                car_lane = 1

    # Draw the background

    screen.fill(WHITE)
    pygame.draw.line(screen, DIVIDER_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    # Draw lanes
    # pygame.draw.line(screen, BLACK, (LANE_WIDTH, 0), (LANE_WIDTH, HEIGHT), 5)
    # pygame.draw.line(
    #     screen, WHITE, (WIDTH - LANE_WIDTH, 0), (WIDTH - LANE_WIDTH, HEIGHT), 5
    # )
    for i in range(1, 5):
        for j in range(0, HEIGHT, 10):
            pygame.draw.rect(screen, BLACK, (i * LANE_WIDTH, j, 2, 5))

    # Draw the ambulance
    ambulance = pygame.image.load("ambulance01.png")
    ambulance = pygame.transform.scale(
        ambulance, (AMBULANCE_WIDTH * 3, AMBULANCE_HEIGHT * 3)
    )
    screen.blit(ambulance, (ambulance_x, ambulance_y))

    # Draw the car
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
