import pygame
import sys
import random
import time

pygame.init()
pygame.font.init()
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h          
screen = pygame.display.set_mode((WIDTH, HEIGHT))
heading_font_style = pygame.font.SysFont('Comic Sans MS', 45)
message_loop = True

BACKGROUND_COLOR = (255, 255, 255)
LANE_COLOR = (0, 0, 0)
CAR1_COLOR = (0, 0, 255)
CAR2_COLOR = (255, 0, 0)
CAR_WIDTH, CAR_HEIGHT = 70, 90
LANE_WIDTH = WIDTH // 4
LANE_COLOR = (0, 0, 0)
CAR_SPEED = 0.5
CAR_SPEED2 = 0.8
CAR_SPEED3 = 1.2
CAR_SPEED4 = 1.5
font = pygame.font.Font(None, 60)

pygame.display.set_caption("Vehicle To Vehicle Communication") 

while message_loop:
    message = heading_font_style.render("Scenario 1: Communicate to peer vehicles in case of Accident Detection", True, (255, 255, 255))
    message_rect = message.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.fill((0, 0, 0))
    screen.blit(message, message_rect)
    pygame.display.flip()
    time.sleep(5)
    message_loop = False

car1_x = 100  
car1_y = HEIGHT - 3 * CAR_HEIGHT
car2_x = (WIDTH - CAR_WIDTH) // 1.2 
car2_y = HEIGHT - 1 * CAR_HEIGHT
car3_x = (WIDTH - CAR_WIDTH) // 2.8
car3_y = HEIGHT - 1 * CAR_HEIGHT

message_loop = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    car1_y -= CAR_SPEED2
    car2_y -= CAR_SPEED3
    car3_y -= CAR_SPEED

    if car3_x > 100:
        car3_x -= CAR_SPEED3
        car3_y -= CAR_SPEED3  
    else:
        accident_occurred = True 
    
    screen.fill(BACKGROUND_COLOR)
    
    for i in range(1, 5):
        for j in range(0, HEIGHT, 10):
            pygame.draw.rect(screen, LANE_COLOR, (i * LANE_WIDTH, j, 2, 5)) 

    car1 = pygame.image.load("car3.png")
    car1 = pygame.transform.scale(car1, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
    screen.blit(car1, (car1_x, car1_y))
    
    car2 = pygame.image.load("car4.png")
    car2 = pygame.transform.scale(car2, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
    screen.blit(car2, (car2_x, car2_y))

    car3 = pygame.image.load("car6.png")
    car3 = pygame.transform.scale(car3, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
    screen.blit(car3, (car3_x, car3_y))
     
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()