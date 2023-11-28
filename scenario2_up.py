import pygame
import sys
import os
import math
import time
import neat

SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016
# Initialize Pygame
pygame.init()
display_info = pygame.display.Info()
WIDTH = 1200
HEIGHT = 720
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 70, 90
car_color = 0
LANE_WIDTH = WIDTH // 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DIVIDER_COLOR = BLACK
#SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
TRACK = pygame.image.load((os.path.join("Assets","newroad2.png")))
# Create the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Change Scenario")
print(TRACK.get_width(),TRACK.get_height())

font = pygame.font.Font(None, 25)

# Set the sprite's speed
car_speed = 2

# Calculate the angle of movement
angle = 45 * math.pi / 180  # Convert degrees to radians

# Initialize the start time
start_time = time.time()




class Car(pygame.sprite.Sprite):
    message_loop = True
    collision_flag = False
    def __init__(self,car_color,initial_position=(250,500), direction_vector=(0,-1)):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets","car.png"))
        print(self.original_image.get_width(),self.original_image.get_height())
        self.original_image = pygame.transform.smoothscale(self.original_image, (CAR_WIDTH,CAR_HEIGHT))
        print("Initial_car_position:", self.original_image.get_width(),self.original_image.get_height())
        self.image = self.original_image
        print("Scaled_car_position:", self.image.get_width(),self.image.get_height())
        #self.rect = self.image.get_rect(center=initial_position)
        self.rect = self.image.get_rect(center=initial_position)
        self.initial_drive_state = False
        self.vel_vector = pygame.math.Vector2(direction_vector)
        self.angle = 0
        self.rotational_vel = 5
        self.direction = 0
        self.alive = True

    def update(self):
        self.drive_car()
        self.rotate_car()
        #for radar_angle in (90):
        self.radar(90)
        self.collision()


    def drive_car(self,speed = 2):
       # if self.initial_drive_state:
            #self.rect.center += self.vec * 4
            #self.rect.center += self.vel_vector * speed
        self.rect.centery += int(self.vel_vector[1] * speed)



    def rotate_car(self):
        if self.direction == 1:
            self.angle -= self.rotational_vel
            self.vel_vector.rotate_ip(self.rotational_vel)
        if self.direction == -1:
            self.angle += self.rotational_vel
            self.vel_vector.rotate_ip(self.rotational_vel)
        #self.image = pygame.transform.rotozoom(self.original_image,self.angle,0.3)

    def radar(self, radar_angle):
        length=0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        try:
            if(x == 1 or y == 1):
                x = 3
                y = 3
               # self.collision_flag = True
            while not SCREEN.get_at((x, y)) == pygame.Color(2, 105,31,255) and length < 200:
            #sys.exit(1)
                length += 1
                x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
                y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
        except IndexError:
            print("Index out of range for pixel", x,y)
        # Draw Radar
        pygame.draw.line(SCREEN, (0, 0, 0, 0), self.rect.center, (x, y), 1)
        pygame.draw.circle(SCREEN, (0, 255, 0, 0), (x, y), 1)


    def collision(self):
        length = 40
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 108)) * length),
                int(self.rect.center[1] - math.sin(math.radians(self.angle + 108)) * length) - (length * 5)]
        collision_point_left= [int(self.rect.center[0] + math.cos(math.radians(self.angle + 68)) * length) 
                                   ,int(self.rect.center[1] - math.sin(math.radians(self.angle + 68)) * length) - (length * 5)]
        # Die on Collision

        if (self.collision_flag == True):
            self.collision_flag = True
            self.message_loop = False
            length -=2
        else:
            self.collision_flag = False
        try:
            if(collision_point_right == [1,1]) or (collision_point_left == [1.1]):
                collision_point_left.x = 2
                collision_point_right.x = 2
                collision_point_left.y = 2
                collision_point_right.y = 2
              #  self.collision_flag = True
        # Access pixels within the valid range
            if SCREEN.get_at(collision_point_right) == pygame.Color(2, 105, 31, 255) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
                self.alive = False
                print("Collision happed")
                self.collision_flag = True
        except IndexError:
            print("Index out of range for pixel", collision_point_left, collision_point_right)
        # Draw Collision Points
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 4)


def running_car():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.blit(TRACK, (0, 0))
        
        # User Input
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car1.sprite.initial_drive_state = False
            car1.sprite.direction = 0

        #We can continuously checking collision flag
        if(car1.sprite.collision_flag == True):
            if(car1.sprite.message_loop == True): 
                print("Message flag true")
                message = font.render(
                    f"Detected object switched lane",
                    True,
                    (255, 255, 255),
                    )
                SCREEN.blit(message, (WIDTH // 1.8, 40))
                time.sleep(5) 
                car1.sprite.message_loop = False  
            car1.sprite.rect.x += car_speed
            car1.sprite.rect.y += car_speed

        #Move car right
            car1.sprite.rect.center += car1.sprite.vel_vector * car_speed 
            car1.sprite.rect.centery += int(car1.sprite.vel_vector[1] * car_speed)
            car1.sprite.rect.centerx += int(car1.sprite.vel_vector[0] * car_speed)
            
        #Update the screen    
        car1.draw(SCREEN)
        car1.update()
        pygame.display.update()

car1 = pygame.sprite.GroupSingle(Car(1))
running_car()