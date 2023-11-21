import pygame
import os

def draw_button(rect, text, color, hover_color, font):
    mouse_pos = pygame.mouse.get_pos()

    pygame.draw.rect(screen, hover_color, rect)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect) 
    
    message = heading_font_style.render("Vehicle To Vehicle Communication System", True, (0, 0, 0))
    message_rect = message.get_rect(center=(WIDTH/2, 100))
    screen.blit(message, message_rect)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def button_action(file_path):
    os.system(f"python {file_path}")

pygame.init()

display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h          
screen = pygame.display.set_mode((WIDTH, HEIGHT))
heading_font_style = pygame.font.SysFont('Comic Sans MS', 45)
pygame.display.set_caption("V2V Communication")


button_color = (255, 255, 255)
hover_color = (220, 220, 220)

center_x = WIDTH // 2  
center_y = HEIGHT // 2 
 
button_spacing = 100

button_width = 200
button_height = 100

x1 = center_x
y1 = center_y - button_spacing * 2

x2 = center_x
y2 = center_y
y2 -= button_height // 2

x3 = center_x
y3 = center_y + button_spacing

button1_rect = pygame.Rect(x1, y1, button_width, button_height)
button2_rect = pygame.Rect(x2, y2, button_width, button_height)
button3_rect = pygame.Rect(x3, y3, button_width, button_height)

button1_text = "Scenario 1"
button2_text = "Scenario 2"
button3_text = "Scenario 3"

font = pygame.font.Font(None, 32)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button1_rect.collidepoint(mouse_pos):
                button_action("scenario1.py")
            elif button2_rect.collidepoint(mouse_pos):
                button_action("scenario12.py")
            elif button3_rect.collidepoint(mouse_pos):
                button_action("scenario3.py")

    screen.fill((255, 255, 255))
    draw_button(button1_rect, button1_text, button_color, hover_color, font)
    draw_button(button2_rect, button2_text, button_color, hover_color, font)
    draw_button(button3_rect, button3_text, button_color, hover_color, font)
    pygame.display.flip()
pygame.quit()
