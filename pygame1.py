'''import pygame
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
run=True
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
pygame.quit()'''
import pygame
pygame.init()

screen = pygame.display.set_mode((400, 300))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))  # Fill the screen with white
    pygame.display.flip()

pygame.quit()
