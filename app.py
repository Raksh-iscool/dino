# DINO GAME AUTOMATION

import cv2
from PIL import ImageGrab
import numpy as np
import pyautogui as pag
import time

'''Class for obtaining the location of the dino and obstacles  '''

class Obstacle:
    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.location = None

# matching objects and finding its location 

    def match(self, scr):
        res = cv2.matchTemplate(scr, self.img, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        startLoc = maxLoc # top left coordinate
        endLoc = (startLoc[0]+self.width, startLoc[1]+self.height) # bottom left coordinate

        if maxVal>0.8:
            self.location = (startLoc, endLoc)
            return True
        else:
            self.location = None
            return False

def grabScreen(bbox=None):
    img = ImageGrab.grab(bbox=bbox)
    img = np.array(img)

    #changing the color as pillow supports [R,G,B] and cv supports [B,G,R]

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    return img

startTime = time.time()
prevTime = time.time()
speedRate = 1.3

# 0 implies that dino is in white screen and 1 implies black screen

player_index = 0
enemy_index = 0

#threashold distance between the dino and the obstacle

distanceThreshold = 120

# Obtaining the locations of the both white & black dino and obstacle 

player =  [Obstacle('Obstacle_Images/dino.png'), Obstacle('Obstacle_Images/blackdino.png')]
enemies = [
      [Obstacle('Obstacle_Images/cactus2.png'), Obstacle('Obstacle_Images/cactus1.png'), Obstacle('Obstacle_Images/bird.png')],
      [Obstacle('Obstacle_Images/blackcactus2.png'), Obstacle('Obstacle_Images/blackcactus1.png'), Obstacle('Obstacle_Images/blackbird.png')],
]

''' Instead of searching the whole window for matching the dino and obstacles, reducing the region to the dino game.
    Matching in large screen takes long time so cropping only the dino game region.
'''

while 1:
    img = grabScreen()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if player[0].match(img):
        topleft_x = int(player[0].location[0][0]- player[0].width)
        topleft_y = int(player[0].location[0][1] - 3*player[0].height)
        bottomRight_x = int(player[0].location[1][0]+14*player[0].width)
        bottomRight_y = int(player[0].location[1][1] + 0.5*player[0].height)
        screenStart = (topleft_x, topleft_y)
        screenEnd = (bottomRight_x, bottomRight_y)
        break

pag.press('space') # initializing the game after the game window is opened

# infinite loop to capture the screen realtime

while 1:
    img_o = grabScreen(bbox=(*screenStart, *screenEnd))
    img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)

    if player[0].match(img):
        player_index = 0
        enemy_index = 0
    elif player[1].match(img):
        player_index = 1
        enemy_index = 1
    
    if time.time() - prevTime > 1:
        if time.time() - startTime < 180 and player[player_index].location:
            distanceThreshold += speedRate # increasing the threshold distance as speed increases
        
        prevTime = time.time()

    # matching the dino and creating a rectangle around it

    if player[player_index].location:
        cv2.rectangle(img_o, player[player_index].location[0], player[player_index].location[1], (255,0,0), 2)
    
    # matching the obstacles and creating a rectangle around it

    for enemy in enemies[enemy_index]:
        if enemy.match(img):
            cv2.rectangle(img_o, enemy.location[0], enemy.location[1], (0,0,255), 2)

            # finding distance between dino and obstacles

            if player[player_index].location:
                horizontalDistance = enemy.location[0][0]-player[player_index].location[1][0] 
                verticalDistance = player[player_index].location[0][1] - enemy.location[1][1]

                # jumping when distance  is less than threshold distance

                if horizontalDistance < distanceThreshold and verticalDistance < 2:
                    pag.press('space')
                    break


    cv2.imshow("Screen", img_o)

    # press q to quit the automation

    if cv2.waitKey(1) == ord('q'):
        break