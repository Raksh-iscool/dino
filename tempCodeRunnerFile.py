import pyautogui
from PIL import Image, ImageGrab
import time
#from numpy import asarray

def hit(key):
    pyautogui.keyDown(key)

def isCollide(data):
    for i in range(350,400):
        for j in range(150,300):
            if data[i,j]<80:
                hit('down')
                return True
    
    for i in range(350,400):
        for j in range(150,400):
            if data[i,j]<80:
                hit('up')
                return True
    return False




#def takeScreenshot():
    
    
    #return image

if __name__=="__main__":
    print('dino starts in 3s')
    time.sleep(2)
    hit('up')
    while True:

        image= ImageGrab.grab().convert('L')
        data=image.load()
        isCollide(data)
    '''#print(asarray(image))
    for i in range(350,400):
        for j in range(150,400):
            data[i,j]=0
    
    for i in range(350,400):
        for j in range(150,300):
            data[i,j]=171
    
    
    image.show()'''