from PIL import ImageGrab, ImageOps
import pyautogui
import win32api
import win32gui
import time
from numpy import array
import random

# CONSTANT VARIABLES
reelChance = 0.9885 
tugChance = 0.9721
CPS = 5
tolerance = 0.28
reactionTime = 0.1

screenRegionTug = (950, 551, 957, 554)
pixelTug = (950, 551)
xTug = 950
yTug = 551
screenRegionRightLeft = (1192, 459, 1193, 473)
pixelRightLeft = (1192, 459)
xTug2 = 1192
yTug2 = 459

def getDesiredWindow():
    """Returns the top-left and bottom-right of the desired window."""
    print('Click the top left of the desired region.')
    pt1 = detectClick()
    print('First position set!')
    time.sleep(1)
    print('Click the bottom right of the desired region.') 
    pt2 = detectClick()
    print('Got the window!')
    return pt1,pt2

def detectClick():
    """Detects and returns the click position"""
    state_left = win32api.GetKeyState(0x01)
    print("Waiting for click...")
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left: #button state changed
            state_left = a
            if a < 0:
                print('Detected left click')
                return win32gui.GetCursorPos()
        time.sleep(0.1)


def getRedPixVal(pt1,pt2):
    """Gets the reference pixel value with the water bob above water."""
    # From the two input points, define the desired box
    box = (pt1[0],pt1[1],pt2[0],pt2[1])
    # Get the image of the desired section
    image = ImageGrab.grab(box)
    # List the red band values of the image (1-d vector) 
    l = list(image.getdata(0))
    # Return the average red band value
    return sum(l)/len(l) 



def fishingLoop():
    """Main fishing loop: gets the desired window and start running the thing."""
    pass


def isTugging():
    r, g, b = pyautogui.pixel(xTug, yTug)
    # print(f"[isTugging] R = {r}, G = {g}, B = {b}.")
    
    if (r, g, b) == (85, 85, 85) or (r, g, b) == (85, 255, 85) or (r, g, b) == (170, 170, 170):
        # print("Tugging detected.")
        return True
    return False


def generateRandomNumber(min, max):
    randomNumber = random.uniform(min, max)
    return round(randomNumber, 2)


def tugging():
    wasLeft = False
    fail = False
    time.sleep(0.15)
    
    # < 5% of Failure
    if generateRandomNumber(0, 100) < 5:
        fail = True
        
    print(f"Tugging Initiated! Success: {not fail}")
    
    while isTugging():
        
        r, g, b = pyautogui.pixel(xTug2, yTug2)
        # print(f"[tugging] R = {r}, G = {g}, B = {b}.")
        
        # Click Left or Right
        if (r, g, b) == (255, 170, 0): # Gold (Left-Click)
            # print("!! LEFT !!")
            if not wasLeft:
                # if fail:
                #     pyautogui.click(button="right")
                #     time.sleep(0.11)
                #     pyautogui.click(button="right")
                #     time.sleep(0.12)
                    
                if generateRandomNumber(0, 100) < 15:
                    pyautogui.click(button="right")  
                time.sleep(generateRandomNumber(0.19, 0.30))
                wasLeft = True
                
            pyautogui.click()
            # if generateRandomNumber(0, 100) < 10: # Misclick on Purpose
            #     pyautogui.click(button="right")
            # else:
            #     pyautogui.click()
        elif (r, g, b) == (85, 255, 255): # Aqua (Right-Click)
            # print("!! RIGHT !!")
            if wasLeft:
                if fail:
                    pyautogui.click()
                    time.sleep(0.11)
                    pyautogui.click()
                    time.sleep(0.12)
                    pyautogui.click()  
                
                if generateRandomNumber(0, 100) < 15:
                    pyautogui.click()
                time.sleep(generateRandomNumber(0.19, 0.31))
                wasLeft = False
                
            pyautogui.click(button="right")    
            # if generateRandomNumber(0, 100) < 10: # Misclick on Purpose
            #     pyautogui.click()
            # else:
            #     pyautogui.click(button="right")
            
        time.sleep(generateRandomNumber(1 / (CPS + tolerance) , 1 / (CPS - tolerance))) 
        
    if wasLeft:
        pyautogui.click()
        time.sleep(0.17)
        pyautogui.click()
        time.sleep(0.22)
        pyautogui.click()
    else:
        pyautogui.click(button="right")
        time.sleep(0.21)
        pyautogui.click(button="right")
    print(f"No Longer Tugging. Purposefully Failed: {fail}")
             
    pass


def afk():
    if generateRandomNumber(0, 100) < 5:
        print("AFK Phase Begins")
        time.sleep(generateRandomNumber(5.12, 10.53))
        print("AFK Phase Ends")


def main():
    """Main function of the MinecraftFisher."""
    print('Running...')

    # Get the window
    pt1, pt2 = getDesiredWindow()
    # Give user grace period of 3 seconds before starting game
    print('Starting minecraft fisher in three seconds...')
    time.sleep(3)
    # Set the reference red pixel value
    refPixVal = getRedPixVal(pt1,pt2)
    print('Ref Pix Val: {}'.format(refPixVal))
    # Main fishing loop
    while True:
        currentRedVal = getRedPixVal(pt1,pt2)
        # print('Fishing... PixValue: {}'.format(round(currentRedVal/refPixVal,2)))
        if currentRedVal < refPixVal * 0.7: 
            # If the bob goes below the water
            print('Fish on reel!')
            # Right-click to reel-in fish
            pyautogui.click(button='right')
            
            time.sleep(0.3)
            
            # Tugging Phase Begins
            tugging()
            
            # Wait for fishing bob to resume its position
            time.sleep(1.5)
            
            # AFK
            afk()
            
            # Right click again to start fishing once again
            print('Casting...')
            pyautogui.click(button='right')
            # Wait for fishing bob to resume its position
            time.sleep(3) 
            
            # If it is still casted
            currentRedVal = getRedPixVal(pt1,pt2)
            if currentRedVal < refPixVal * 0.7:
                pyautogui.click(button='right')
                time.sleep(3)
                
            time.sleep(2)

        time.sleep(0.35)


if __name__ == '__main__':
    main()