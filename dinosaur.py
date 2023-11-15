# ... (previous code)
import pygame
import os
import random
pygame.init()

SCREEN_HEIGHT=600
SCREEN_WIDTH=500
SCREEN= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
RUNNING=[pygame.image.load(os.path.join("dinol.png")),pygame.image.load(os.path.join("dinor.png"))]
DUCKING=[pygame.image.load(os.path.join("dino_ducking1.png")),pygame.image.load(os.path.join("dino_ducking2.png"))]
JUMPING=[pygame.image.load(os.path.join("dino.png"))]
SMALL_CACTUS=[pygame.image.load(os.path.join("cactus-small.png"))]
LARGE_CACTUS=[pygame.image.load(os.path.join("cactus-big.png"))]
BIRD=[pygame.image.load(os.path.join("birds.png"))]
CLOUD=[pygame.image.load(os.path.join("cloud.png"))]
BG=[pygame.image.load(os.path.join("track2f.png"))]
class Dinosaur():
    X_Pos = 80
    Y_Pos = 310
    Y_Pos_DUCK=340
    JUMP_VEL=8.5
    

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel=self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Pos
        self.dino_rect.y = self.Y_Pos

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect=self.image.get_rect()
        self.dino_rect.x = self.X_Pos
        self.dino_rect.y = self.Y_Pos_DUCK
          # Update X position without resetting Y position'''
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect=self.image.get_rect()
        self.dino_rect.x = self.X_Pos
        self.dino_rect.y = self.Y_Pos
          # Update X position without resetting Y position'''
        self.step_index += 1
        '''if self.step_index // 5 < len(self.run_img):  # Check if the index is within the list range
            self.image = self.run_img[self.step_index // 5]
        else:
            self.step_index = 0  # Reset the index if it exceeds the list length
            self.image = self.run_img[self.step_index // 5]

        self.step_index += 1
        self.dino_rect.x = self.X_Pos'''  # Update X position without resetting Y position


    def jump(self):
        self.image=self.jump_img
        if self.dino_jump:
            self.dino_rect.y -=int( self.jump_vel * 4)
            self.jump_vel -= 0.8
        if self.jump_vel< -self.JUMP_VEL:
            self.dino_jump= False
            self.jump_vel=self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x=SCREEN_WIDTH + random.randint(800,1000)
        self.y=random.randint(50,100)
        self.image=CLOUD[0]
        self.width= self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x=SCREEN_WIDTH + random.randint(2500,3000)
            self.y=random.randint(50,100)

    
    def draw(self,SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

def main():
    global game_speed, x_pos_bg, y_pos_bg
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud=Cloud()  # Create an instance of the Dinosaur class
    game_speed=14
    x_pos_bg=0
    y_pos_bg=380

    def background():
        global x_pos_bg, y_pos_bg,BG
        image_width= BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg=0
        x_pos_bg-=game_speed
    '''def background():
        global x_pos_bg, y_pos_bg, SCREEN, game_speed, BG

    # Example assuming BG is a list of images or surfaces
        image_widths = [image.get_width() for image in BG]
    
    # Your remaining code using image_widths as needed
    # ...

    # Example usage:
        for i, image in enumerate(BG):
            SCREEN.blit(image, (x_pos_bg + i * 5*image_widths[i], y_pos_bg))
        # Additional processing using image_widths[i] or image, etc.
'''
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        background()

        cloud.draw(SCREEN)
        cloud.update()
        
        clock.tick(30)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
