import pygame
import sys
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
LANE_WIDTH = WIDTH // 8
LANE_COLOR = (0, 0, 0)
car4_timer = 400
car5_timer = 650
car6_timer = 600
CAR_SPEED = 0.5
CAR_SPEED2 = 0.7  
CAR_SPEED3 = 1.0
CAR_SPEED4 = 0.9
CAR3_SPEED = 1.1
CAR6_SPEED = 0.8

font = pygame.font.Font(None, 25)
pygame.display.set_caption("Vehicle To Vehicle Communication")

while message_loop:
    message = heading_font_style.render(
        "Scenario 1: Communicate to peer vehicles in case of Accident Detection", True, (255, 255, 255)
    )
    message_rect = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.fill((0, 0, 0))
    screen.blit(message, message_rect)
    pygame.display.flip()
    time.sleep(3)
    message_loop = False

clock = pygame.time.Clock()

car1_x = 30
car1_y = HEIGHT - 3 * CAR_HEIGHT
car2_x = (WIDTH - CAR_WIDTH) // 3.4
car2_y = HEIGHT - 1 * CAR_HEIGHT
car3_x = (WIDTH - CAR_WIDTH) // 2.5
car3_y = HEIGHT - 1 * CAR_HEIGHT
car6_x = (WIDTH - CAR_WIDTH) // 2.5
car6_y = HEIGHT - 1 * CAR_HEIGHT + 150
car4_x = 20
car4_y = HEIGHT - 3 * CAR_HEIGHT + 300
car5_x = 20
car5_y = HEIGHT - 3 * CAR_HEIGHT + 350

message_loop = True
accident_occurred = False

car4_switch = False
car5_switch = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    if (accident_occurred == False):
        car1_y -= CAR_SPEED2
        car2_y -= CAR_SPEED3
    
    if (car1_y < 400 and accident_occurred == False):
        car2_x -= CAR_SPEED3

    if car4_timer > 0:
        car4_timer -= 1
    else:
        if (car4_y <= car1_x + 375 or car4_y <= car2_x + 375) and car4_x < (WIDTH - CAR_WIDTH) // 6.8 + 10:
            if (car4_switch == False):
                message = font.render(
                    f"Yellow car switching to lane 2.",
                    True,
                    (0, 0, 0),
                )
                car4_switch = True
            screen.blit(message, (WIDTH // 1.8, 40))
            pygame.display.flip()
            car4_x += CAR_SPEED2
        car4_y -= CAR_SPEED2
    if car5_timer > 0:
        car5_timer -= 1
    else:
        if (car5_y <= car1_x + 600 or car5_y <= car2_x + 600) and car5_x < (WIDTH - CAR_WIDTH) // 6.8 + 10:
            if (car5_switch == False):
                message = font.render(
                    f"Red car switching to lane 2.",
                    True,
                    (0, 0, 0),
                )
                car5_switch = True
            screen.blit(message, (WIDTH // 1.8, 40))
            pygame.display.flip()
            car5_x += CAR_SPEED
        car5_y -= CAR_SPEED
    
    if car6_timer > 0:
        car6_timer -= 1
    else:
        car6_y -= CAR6_SPEED

    car3_y -= CAR3_SPEED
    if accident_occurred == False and car1_x < car2_x + CAR_WIDTH and car1_x + CAR_WIDTH > car2_x and car1_y < car2_y + CAR_HEIGHT and car1_y + CAR_HEIGHT > car2_y:
        accident_occurred = True
        message = font.render(
            f"Accident Detected by yellow car on lane 1.",
            True,
            (0, 0, 0),
        )
        screen.blit(message, (WIDTH // 1.8, 10))
        pygame.display.flip()
        time.sleep (1)
        message = font.render(
            f"Car Yellow informs other cars on lane 1 about accident.",
            True,
            (0, 0, 0),
        )
        screen.blit(message, (WIDTH // 1.8, 40))
        pygame.display.flip()
        time.sleep (1)
    else:
        screen.fill(BACKGROUND_COLOR)

        for i in range(1, 5):
            for j in range(0, HEIGHT, 10):
                pygame.draw.rect(screen, LANE_COLOR, (i * LANE_WIDTH, j, 2, 5))

        car4 = pygame.image.load("car04.png") 
        car4 = pygame.transform.scale(car4, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
        screen.blit(car4, (car4_x, car4_y))

        car5 = pygame.image.load("car01.png")
        car5 = pygame.transform.scale(car5, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
        screen.blit(car5, (car5_x, car5_y))

        car1 = pygame.image.load("car01.png")
        car1 = pygame.transform.scale(car1, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
        screen.blit(car1, (car1_x, car1_y))

        car2 = pygame.image.load("car06.png")
        car2 = pygame.transform.scale(car2, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
        screen.blit(car2, (car2_x, car2_y))

        car3 = pygame.image.load("car04.png")
        car3 = pygame.transform.scale(car3, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
        screen.blit(car3, (car3_x, car3_y))

        car6 = pygame.image.load("car06.png")
        car6 = pygame.transform.scale(car6, (CAR_WIDTH * 2, CAR_HEIGHT * 2))
        screen.blit(car6, (car6_x, car6_y))

        pygame.display.flip()
        clock.tick(60)
