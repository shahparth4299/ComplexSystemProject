import pygame
import sys
import os
import math
import time
SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016
# Initialize Pygame
pygame.init()
display_info = pygame.display.Info()
WIDTH = 1200
HEIGHT = 720
FPS = 30
LANE_WIDTH = 150 #Lane Width
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POTHOLE = (0, 164,235,255)
RAIN_COLOR = (135, 206, 235)  # Light blue color for raindrops


#Create Track
TRACK = pygame.image.load((os.path.join("Assets","newroad3.png")))
# Create the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Change Scenario")

font = pygame.font.Font(None, 25)
CAR_WIDTH, CAR_HEIGHT = 70, 90
# Set the sprite's speed
#Calculate the angle of movement
angle = 45 * math.pi / 180  # Convert degrees to radians


# Initialize the start time
start_time = time.time()

class Base_station():
    collision_detected = 0
    reduced_all_cars = False
    def __init__(self):
        super().__init__()
 

    def broadcast_message(self,collision_detected):
        if(collision_detected == 1):
            message = font.render(
                f"Base station receive a message Blocked Lane due to bad weather",
                True,
                (255, 255, 255),
            )
            SCREEN.blit(message, (WIDTH // 1.8, 70))
            pygame.display.flip()
            time.sleep(2)
            self.reduced_all_cars = True
            message = font.render(
                f"Send message to all cars to reduce speed",
                True,
                (255, 255, 255),
            )
            SCREEN.blit(message, (WIDTH // 1.8, 90))
            pygame.display.flip()
            time.sleep(2)
        if(collision_detected == 2):
            message = font.render(
                f"Base station receive a message of bad weather",
                True,
                (255, 255, 255),
            )
            SCREEN.blit(message, (WIDTH // 1.8, 70))
            pygame.display.flip()
            self.reduced_all_cars = True
            message = font.render(
                f"Send message to all cars to reduce speed",
                True,
                (255, 255, 255),
            )
            SCREEN.blit(message, (WIDTH // 1.8, 90))
            pygame.display.flip()


