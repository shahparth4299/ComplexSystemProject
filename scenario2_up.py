import pygame
import sys
import os
import math
import time
import random
from Car import Car
from Global_System import *
# Raindrops list
raindrops = []
def scenario_two():
    # Load the background music
    pygame.mixer.music.load(
        "rain_sound.mp3"
    )  # Replace 'background_music.mp3' with your audio file

    # Play the background music (-1 to loop indefinitely)
    pygame.mixer.music.play(-1)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.blit(TRACK, (0, 0))
        # Create new raindrops
        for i in range(40):  # Adjust the number of raindrops per frame
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
                SCREEN, RAIN_COLOR, (x, y), (x, y + 2), 1
            )  # Adjust the line length and thickness
            car_center = [car1.sprite.rect.x,car1.sprite.rect.y]
            if SCREEN.get_at(car_center) == pygame.Color(RAIN_COLOR):
                Car.bad_weather_flag = True
                if (car1.sprite.rect.x == x and car1.sprite.rect.y == y):
                    print("coordinate match")
                    #sys.exit(1)
        # Update the display
        pygame.display.flip()

     #We can continuously checking collision flag
        if(Car.bad_weather_flag == True):
            message = font.render(
                    f"Bad weather detected",
                    True,
                    (255, 255, 255),
                    )
            SCREEN.blit(message, (WIDTH // 1.8, 40))
            car1.draw(SCREEN)
            car2.draw(SCREEN)
            car3.draw(SCREEN)
            pygame.display.update()
            base1.broadcast_message(2)
            if(base1.reduced_all_cars == True):
                Car.speed_reduce = True

        if(car1.sprite.collision_flag == True and car1.sprite.lane_distance > 0):
            if(car1.sprite.message_loop == True): 
                message = font.render(
                    f"Detected object switched lane",
                    True,
                    (255, 255, 255),
                    )
                SCREEN.blit(message, (WIDTH // 1.8, 40))
                car1.draw(SCREEN)
                car2.draw(SCREEN)
                car3.draw(SCREEN)
                pygame.display.update()
                time.sleep(3) 
                base1.broadcast_message(1)
                if(base1.reduced_all_cars == True):
                    Car.speed_reduce = True
                car1.sprite.message_loop = False  
            car1.sprite.rect.x += car1.sprite.reduced_speed
            car1.sprite.rect.y += car1.sprite.reduced_speed
            car1.sprite.lane_distance -= car1.sprite.reduced_speed
        #Move car right
            car1.sprite.rect.center += car1.sprite.vel_vector * car1.sprite.reduced_speed
            car1.sprite.rect.centery += int(car1.sprite.vel_vector[1] * car1.sprite.reduced_speed)
            car1.sprite.rect.centerx += int(car1.sprite.vel_vector[0] * car1.sprite.reduced_speed)

        #Update the screen    
        car1.draw(SCREEN)
        car1.update()
        car2.draw(SCREEN)
        car2.update()
        car3.draw(SCREEN)
        car3.update()


        pygame.display.update()

car1 = pygame.sprite.GroupSingle(Car(1,"car.png",(250,600),2,1))
car2 = pygame.sprite.GroupSingle(Car(2,"car.png",(750,600),2,1))
car3 = pygame.sprite.GroupSingle(Car(3,"car.png",(1050,600),2,1))
base1 = Base_station()
scenario_two()