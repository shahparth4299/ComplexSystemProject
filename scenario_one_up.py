import pygame
import sys
import time
from Car import Car
from Global_System import *

TRACK = pygame.image.load((os.path.join("Assets","newroad_Screen.png")))
car4 = None
car5 = None

def scenario_one():

    clock = pygame.time.Clock()

    message_loop = True
    accident_occurred = False

    car4_switch = False
    car5_switch = False
    flag = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        SCREEN.blit(TRACK, (0, 0))

   
        if accident_occurred == False:
            if car1.sprite.rect.y < 500 and Car.accident_occured == False:
                if flag:
                    pygame.mixer.music.load(
                        "accident_sound.mp3"
                    )  # Replace 'background_music.mp3' with your audio file

                    # Play the background music (-1 to loop indefinitely)
                    pygame.mixer.music.play(-1)
                    flag = False
                car2.sprite.rect.x -= 1
            # Load the background music

        if (Car.accident_occured == False
            and car2.sprite.rect.x - car1.sprite.rect.x < 20
        ):
            print("Accident Happened", car1.sprite.rect.x, car2.sprite.rect.x)
            Car.accident_occured = True
            car1.sprite.accident_happen = True
            car2.sprite.accident_happen = True
            car4.sprite.collision_flag = True
            message = font.render(
                f"Accident Detected by Car 4 on lane 1.",
                True,
                BLACK,
            )
            SCREEN.blit(message, (WIDTH // 1.3, 40))
            
        if(car4.sprite.collision_flag == True and car4.sprite.lane_distance > 0):
            #if(car4.sprite.message_loop == True): 
            message = font.render(
            f"Car 4 informs base station about accident.",
            True,
            (0, 0, 0),
            )
            SCREEN.blit(message, (WIDTH // 1.3, 60))
            car1.draw(SCREEN)
        
            car2.draw(SCREEN)
      
            car3.draw(SCREEN)
      
            car4.draw(SCREEN)
            base1.broadcast_message(1)
            car4.sprite.rect.x += car4.sprite.reduced_speed
            car4.sprite.rect.y += car4.sprite.reduced_speed
            car4.sprite.lane_distance -= car4.sprite.reduced_speed
        #Move car right
            car4.sprite.rect.center += car4.sprite.vel_vector * car4.sprite.reduced_speed
            car4.sprite.rect.centery += int(car4.sprite.vel_vector[1] * car4.sprite.reduced_speed)
            car4.sprite.rect.centerx += int(car4.sprite.vel_vector[0] * car4.sprite.reduced_speed)

 #Update the screen    
        car1.draw(SCREEN)
        car1.update()
        car2.draw(SCREEN)
        car2.update()
        car3.draw(SCREEN)
        car3.update()
        car4.draw(SCREEN)
        car4.update()
 #           car5.draw(SCREEN)
  #          car5.update()
        pygame.display.update()


"""
        if (Car.accident_occured == False
            and car1.sprite.rect.x < car2.sprite.rect.x + CAR_WIDTH
            and car1.sprite.rect.x + CAR_WIDTH > car2.sprite.rect.x
            and car1.sprite.rect.y < car2.sprite.rect.y + CAR_HEIGHT
            and car1.sprite.rect.y + CAR_HEIGHT > car2.sprite.rect.y
        ):
    
        if (car4 != None):
            if ((car4.sprite.rect.y <= car1.sprite.rect.x + 375 or car4.sprite.rect.y <= car2.sprite.rect.x + 375) 
                and car4.sprite.rect.x < (WIDTH - CAR_WIDTH)) // 6.8 + 10:
                if car4_switch == False:
                    message = font.render(
                        f"Yellow Car: Accident Detected in lane 4. Switching to lane 3",
                        True,
                        (0, 0, 0),
                    )
                    car4_switch = True
                screen.blit(message, (WIDTH // 1.8, 40))
                pygame.display.flip()
                car4.sprite.rect.x += CAR_SPEED2
            car4.sprite.rect.y -= CAR_SPEED2
            if ((car5.sprite.rect.y <= car1.sprite.rect.x + 600 or car5.sprite.rect.y <= car2.sprite.rect.x + 600) 
                and car5.sprite.rect.x < (WIDTH - CAR_WIDTH)) // 6.8 + 10:
                if car5_switch == False:
                    message = font.render(
                        f"Red Car: Acknowledged. Switching to lane 2.",
                        True,
                        (0, 0, 0),
                    )
                    car5_switch = True
                screen.blit(message, (WIDTH // 1.8, 40))
                pygame.display.flip()
                car5.sprite.rect.x += CAR_SPEED
            car5.sprite.rect.y -= CAR_SPEED

        car3.sprite.rect.y -= CAR3_SPEED
       
            message = font.render(
                f"Car Yellow informs other cars on lane 1 about accident.",
                True,
                (0, 0, 0),
            )
            screen.blit(message, (WIDTH // 1.8, 40))
            pygame.display.flip()
            time.sleep(1)
        else:

            pygame.display.flip()
            clock.tick(60)
"""
    
car1 = pygame.sprite.GroupSingle(Car(1,"car.png",(150,600),1,1,CAR_WIDTH,CAR_HEIGHT))
car2 = pygame.sprite.GroupSingle(Car(2,"car.png",(350,550),1,1,CAR_WIDTH,CAR_HEIGHT))
car3 = pygame.sprite.GroupSingle(Car(3,"car3.png",(550,600),2,1,CAR_WIDTH,CAR_HEIGHT))
car4 = pygame.sprite.GroupSingle(Car(4,"car4.png",(150,900),1,1,CAR_WIDTH,CAR_HEIGHT))
#car5 = pygame.sprite.GroupSingle(Car(5,"car.png",(150,1000),1,1,CAR_WIDTH,CAR_HEIGHT))

base1 = Base_station()

scenario_one()