import pygame
import sys
import os
import math
import time

from Global_System import *
MAX_RADAR_LENGTH = 200
MIN_RADAR_LENGTH = 40
WEATHER_SENSOR_LENGTH = 10
class Car(pygame.sprite.Sprite):
    message_loop = True
    collision_flag = False
    lane_distance = LANE_WIDTH
    speed_reduce = False
    bad_weather_flag = False
    accident_occured = False
    def __init__(self,number,car_image,initial_position, car_speed, reduced_speed, car_width,car_height,direction_vector=(0,-1)):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets",car_image))
        print(self.original_image.get_width(),self.original_image.get_height())
        self.original_image = pygame.transform.smoothscale(self.original_image, (car_width,car_height))
        print("Initial_car_position:", self.original_image.get_width(),self.original_image.get_height())
        self.image = self.original_image
        print("Scaled_car_position:", self.image.get_width(),self.image.get_height())
        self.rect = self.image.get_rect(center=initial_position)
        self.initial_drive_state = False
        self.vel_vector = pygame.math.Vector2(direction_vector)
        self.angle = 0
        self.rotational_vel = 5
        self.direction = 0
        self.alive = True
        self.speed = car_speed
        self.reduced_speed = reduced_speed
        self.car_number = number
        self.accident_happen = False

    def update(self):
        if (self.accident_happen == False):
            self.drive_car()

        self.rotate_car()
        self.radar(90)
        self.collision()
        self.collision_car()
        self.weather_sensor()

    #Currently speed is constant in y-axis only
    def drive_car(self):
        if(self.speed_reduce == True):
            self.rect.centery += int(self.vel_vector[1] * self.reduced_speed)
        else:
            self.rect.centery += int(self.vel_vector[1] * self.speed)
        
    def rotate_car(self):
        if self.direction == 1:
            self.angle -= self.rotational_vel
            self.vel_vector.rotate_ip(self.rotational_vel)
        if self.direction == -1:
            self.angle += self.rotational_vel
            self.vel_vector.rotate_ip(self.rotational_vel)

    #We are detecting the pothole
    def radar(self, radar_angle):
        length=0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        try:
            if(x < 1):
                x = 2
            if(y < 1):
                y = 2
            while not SCREEN.get_at((x, y)) == pygame.Color(POTHOLE) and length < MAX_RADAR_LENGTH:
                length += 1
                x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
                y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
        except IndexError:
                pass

        # Draw Radar
        #pygame.draw.line(SCREEN, BLACK, self.rect.center, (x, y), 1)
        #pygame.draw.circle(SCREEN, BLACK, (x, y), 1)


    def collision(self):
        length = 40
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 108)) * length),
                int(self.rect.center[1] - math.sin(math.radians(self.angle + 108)) * length) - (length * 6)]
        collision_point_left= [int(self.rect.center[0] + math.cos(math.radians(self.angle + 68)) * length) 
                                   ,int(self.rect.center[1] - math.sin(math.radians(self.angle + 68)) * length) - (length * 6)]
        # Die on Collision

        if (self.collision_flag == True):
            self.collision_flag = True
            self.message_loop = False
            length -=2
        else:
            self.collision_flag = False
        try:
            if((collision_point_right[0] < 1) or (collision_point_left[0] < 1) 
            or (collision_point_right[1] < 1) or (collision_point_left[1] < 1)
            or collision_point_right[0] > WIDTH or  collision_point_right[1] > HEIGHT
                or collision_point_left[0] > WIDTH or  collision_point_left[1] > HEIGHT):
                collision_point_left[0] = 2
                collision_point_right[0] = 2
                collision_point_left[1] = 2
                collision_point_right[1] = 2
                #  self.collision_flag = True
            # Access pixels within the valid range
            if SCREEN.get_at(collision_point_right) == pygame.Color(POTHOLE) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(POTHOLE):
                self.alive = False
                self.collision_flag = True
        except IndexError:
            pass
            #print("Index out of range for pixel", collision_point_left, collision_point_right)
        # Draw Collision Points
        #pygame.draw.circle(SCREEN, BLACK, collision_point_right, 4)
        #pygame.draw.circle(SCREEN, BLACK, collision_point_left, 4)


    def collision_car(self):
        length = MIN_RADAR_LENGTH
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 108)) * length),
                int(self.rect.center[1] - math.sin(math.radians(self.angle + 108)) * length) - (length * 2)]
        collision_point_left= [int(self.rect.center[0] + math.cos(math.radians(self.angle + 68)) * length) 
                                   ,int(self.rect.center[1] - math.sin(math.radians(self.angle + 68)) * length) - (length * 2)]
        # Die on Collision

        if (self.collision_flag == True):
            self.collision_flag = True
            self.message_loop = False
            length -=2
        else:
            self.collision_flag = False
        try:
            if((collision_point_right[0] < 1) or (collision_point_left[0] < 1) 
            or (collision_point_right[1] < 1) or (collision_point_left[1] < 1)
            or collision_point_right[0] > WIDTH or  collision_point_right[1] > HEIGHT
                or collision_point_left[0] > WIDTH or  collision_point_left[1] > HEIGHT):
                collision_point_left[0] = 2
                collision_point_right[0] = 2
                collision_point_left[1] = 2
                collision_point_right[1] = 2
                #  self.collision_flag = True
            # Access pixels within the valid range
            if ((Car.accident_occured == True) and (SCREEN.get_at(collision_point_right) == pygame.Color(CAR_COLOR) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(CAR_COLOR))):
                self.alive = False
                self.collision_flag = True
                message = font.render(
                f"Accident Detected by Car 4 on lane 1. Switch Lane",
                True,
                BLACK,
                )
                SCREEN.blit(message, (WIDTH // 1.3, 40))
        except IndexError:
            pass
        # Draw Collision Points
        pygame.draw.circle(SCREEN, RED, collision_point_right, 4)
        pygame.draw.circle(SCREEN, RED, collision_point_left, 4)

    def collision_resolver(self):
        distanced_moved = MAX_RADAR_LENGTH
        if(self.collision_flag == True):
            if(self.message_loop == True): 
                message = font.render(f"Detected object switch lane", True, BLACK)
                SCREEN.blit(message, (WIDTH // 1.3, 40))
                time.sleep(3) 
            while(distanced_moved > 30):
                self.rect.x += self.reduced_speed
                self.rect.y += self.reduced_speed

                #Move car right
                self.rect.center += self.vel_vector * self.reduced_speed 
                self.rect.centery += int(self.vel_vector[1] * self.reduced_speed)
                self.rect.centerx += int(self.vel_vector[0] * self.reduced_speed)
                distanced_moved = distanced_moved - self.speed
                self.draw(SCREEN)
                self.update()
                pygame.display.update()

    def weather_sensor(self):
        length = WEATHER_SENSOR_LENGTH
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 108)) * length),
                int(self.rect.center[1] - math.sin(math.radians(self.angle + 108)) * length) - (length)]
        collision_point_left= [int(self.rect.center[0] + math.cos(math.radians(self.angle + 68)) * length) 
                                   ,int(self.rect.center[1] - math.sin(math.radians(self.angle + 68)) * length) - (length)]
        try:
            if((collision_point_right[0] < 1) or (collision_point_left[0] < 1) 
                or (collision_point_right[1] < 1) or (collision_point_left[1] < 1)
                or collision_point_right[0] > WIDTH or  collision_point_right[1] > HEIGHT
                    or collision_point_left[0] > WIDTH or  collision_point_left[1] > HEIGHT):
                    collision_point_left[0] = 2
                    collision_point_right[0] = 2
                    collision_point_left[1] = 2
                    collision_point_right[1] = 2
                   # print(collision_point_left[0],collision_point_left[1],collision_point_right[0],collision_point_right[1])
            # Access pixels within the valid range
            if SCREEN.get_at(collision_point_right) == pygame.Color(RAIN_COLOR) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(RAIN_COLOR):
                Car.bad_weather_flag = True
        except IndexError:
            pass
            #print("Index out of range for pixel", collision_point_left, collision_point_right)
        # Draw Collision Points
        pygame.draw.circle(SCREEN, WHITE, collision_point_right, 4)
        pygame.draw.circle(SCREEN, WHITE, collision_point_left, 4)
