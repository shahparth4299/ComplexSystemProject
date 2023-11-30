import pygame
import sys
import os
import math
import time
from Car import Car
from Global_System import *
AMBULANCE_SPEED = 3
AMBULANCE_Y = 100 + 50
AMBULANCE_TIMER = 300  # Introduce ambulance 1 second earlier
AMBULANCE_WIDTH, AMBULANCE_HEIGHT = 120, 110
AMBULANCE_CAR_DIST = 180

#Create Track
TRACK = pygame.image.load((os.path.join("Assets","newroad_Screen.png")))
def running_car_scenario3():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.blit(TRACK, (0, 0))
       #Update the screen    
        car1.draw(SCREEN)
        car1.update()
        ambulance.draw(SCREEN)
        ambulance.update()
        car3.draw(SCREEN)
        car3.update()

        pygame.display.update()

        if ((ambulance.sprite.rect.y - car1.sprite.rect.y < AMBULANCE_CAR_DIST) and car1.sprite.lane_distance > 0):
            if(car1.sprite.message_loop == True): 
                message = font.render(
                    f"Emergency vehicle in back switch lane switched lane",
                    True,
                    BLACK,
                    )
                SCREEN.blit(message, (WIDTH // 1.3, 40))
                car1.draw(SCREEN)
                ambulance.draw(SCREEN)
                car3.draw(SCREEN)
                pygame.display.update()
                time.sleep(3) 
                car1.sprite.message_loop = False  
            car1.sprite.rect.x += car1.sprite.reduced_speed
            car1.sprite.rect.y += car1.sprite.reduced_speed
            car1.sprite.lane_distance -= car1.sprite.reduced_speed
        #Move car right
            car1.sprite.rect.center += car1.sprite.vel_vector * car1.sprite.reduced_speed
            car1.sprite.rect.centery += int(car1.sprite.vel_vector[1] * car1.sprite.reduced_speed)
            car1.sprite.rect.centerx += int(car1.sprite.vel_vector[0] * car1.sprite.reduced_speed)


car1 = pygame.sprite.GroupSingle(Car(1,"car.png",(110,500),1,1,CAR_WIDTH,CAR_HEIGHT))
ambulance = pygame.sprite.GroupSingle(Car(2,"ambulance.png",(110,700),2,1,AMBULANCE_WIDTH, AMBULANCE_HEIGHT))
car3 = pygame.sprite.GroupSingle(Car(3,"car.png",(550,700),2,1,CAR_WIDTH,CAR_HEIGHT))
base1 = Base_station()
running_car_scenario3()

 