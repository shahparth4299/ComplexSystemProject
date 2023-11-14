import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (255, 255, 255)
CAR1_COLOR = (0, 0, 255)
CAR2_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (255, 255, 0)
CAR_WIDTH, CAR_HEIGHT = 30, 60
OBSTACLE_RADIUS = 15
LANE_WIDTH = 100
LANE_COLOR = (0, 0, 0)
CAR_SPEED = 0.5
font = pygame.font.Font(None, 25)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Initialize positions
car1_x = (WIDTH - CAR_WIDTH) // 2
car1_y = HEIGHT - 3 * CAR_HEIGHT
car2_x = (WIDTH - CAR_WIDTH) // 2
car2_y = HEIGHT - 1 * CAR_HEIGHT
# obstacle_x = random.randint(0, WIDTH - OBSTACLE_RADIUS * 2)
obstacle_x = WIDTH - OBSTACLE_RADIUS * 20
obstacle_y = 0

message_loop = True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the obstacle
    obstacle_y += CAR_SPEED

    # Check for obstable

    if (car1_y - obstacle_y) <= 200:
        while message_loop:
            message = font.render(
                f"Car 1: There is a collision ahead in 2 kilometers in lane 2.",
                True,
                (0, 0, 0),
            )
            screen.blit(message, (10, 10))
            pygame.display.flip()
            message = font.render(
                f"I am changing to lane 3.",
                True,
                (0, 0, 0),
            )
            screen.blit(message, (10, 40))
            pygame.display.flip()
            time.sleep(2)
            message = font.render(
                f"Car 2: Message acknowleged. Changing to lane 1.", True, (0, 0, 0)
            )

            screen.blit(message, (10, 70))
            pygame.display.flip()
            time.sleep(2)
            message = font.render(
                f"Base Station: Message acknowleged. Sending help.", True, (0, 0, 0)
            )

            screen.blit(message, (10, 100))
            pygame.display.flip()
            time.sleep(2)
            message_loop = False

        print("car1_y = " + str(car1_y))
        print(
            "Broadcast message - There is a collision ahead in 2 kilometers in lane 2. I am changing to lane 3."
        )
        print("Car 2 - Message acknowleged. Changing to lane 1.")
        car2_x = (WIDTH - CAR_WIDTH) // 4
        car2_y = HEIGHT - 1 * CAR_HEIGHT
        car1_x = (WIDTH - CAR_WIDTH) // 1.2
        car1_y = HEIGHT - 3 * CAR_HEIGHT

    # Update the screen
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, CAR1_COLOR, (car1_x, car1_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.rect(screen, CAR2_COLOR, (car2_x, car2_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.circle(
        screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y), OBSTACLE_RADIUS
    )

    # Draw vertical lines between lanes
    # for i in range(1, 4):
    #     pygame.draw.rect(screen, LANE_COLOR, (i * LANE_WIDTH, 0, 2, HEIGHT))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
