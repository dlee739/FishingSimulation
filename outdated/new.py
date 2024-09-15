from PIL import ImageGrab, ImageOps
import pyautogui
import win32api
import win32gui
import time
from numpy import array
import numpy as np
import random
import cv2

# CONSTANT VARIABLES
reelChance = 0.9885 
tugChance = 0.9721
CPS = 5.2
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
sRegionInventory = (793, 577, 1126, 691)
sRegionBucket = (790, 333, 1126, 560)

cursor_neutral = (31, 44)

IMAGE_EMPTY = "inv_empty.png"
IMAGE_FISH = "fish.png"

s1Full = False
s2Full = False
s3Full = False
s1Key = '2'
s2Key = '3'
s3Key = '4'
poleKey = '1'
s1LastSlot = (1084, 516, 1124, 557)
s2LastSlot = (1045, 476, 1092, 525)
s3LastSlot = (1083, 443, 1125, 486)


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
    if generateRandomNumber(0, 100) < 13:
        fail = True
        
    print(f"Tugging Initiated! Success: {not fail}")
    
    changesDirection = 0
    while isTugging():
        if changesDirection >= 7:
            chanceFail = (pow(changesDirection - 6, 2.5) / 100) * 100 + 1
            if generateRandomNumber(0, 100) <= chanceFail:
                fail = True
        
        sleepTime = generateRandomNumber(1 / (CPS + tolerance) , 1 / (CPS - tolerance)) # Initial Sleep Time
        
        r, g, b = pyautogui.pixel(xTug2, yTug2)
        # print(f"[tugging] R = {r}, G = {g}, B = {b}.")
        
        # Click Left or Right
        if (r, g, b) == (255, 170, 0): # Gold (Left-Click)
            # print("!! LEFT !!")
            if not wasLeft:
                if fail:
                    pyautogui.click(button="right")
                    time.sleep(0.11)
                    pyautogui.click(button="right")
                    time.sleep(0.12)
                    pyautogui.click(button="right")
                    
                if generateRandomNumber(0, 100) < 15:
                    pyautogui.click(button="right")  
                time.sleep(generateRandomNumber(1 / (CPS - 1.5 + tolerance) , 1 / (CPS - 1.5 - tolerance)))
                wasLeft = True
                changesDirection += 1
                
            pyautogui.click()
            # if generateRandomNumber(0, 100) < 10: # Misclick on Purpose
            #     pyautogui.click(button="right")
            # else:
            #     pyautogui.click()
            
            sleepTime = generateRandomNumber(1 / (CPS + 0.2 + tolerance) , 1 / (CPS + 0.2 - tolerance)) # Change CPS for consecutive
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
                time.sleep(generateRandomNumber(1 / (CPS - 1.5 + tolerance) , 1 / (CPS - 1.5 - tolerance)))
                wasLeft = False
                changesDirection += 1
                
            pyautogui.click(button="right")    
            # if generateRandomNumber(0, 100) < 10: # Misclick on Purpose
            #     pyautogui.click()
            # else:
            #     pyautogui.click(button="right")
            sleepTime = generateRandomNumber(1 / (CPS + 0.2 + tolerance) , 1 / (CPS + 0.2 - tolerance)) # Change CPS for consecutive
        
           
        time.sleep(sleepTime) 
        
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
        
        
# Function to take a screenshot of a selected region
def take_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert to OpenCV format
    return screenshot


# Function to detect duplicates of the symbol
def detect_symbols(region, screenshot, symbol_path, threshold=0.95):
    # Load the symbol image
    symbol = cv2.imread(symbol_path, cv2.IMREAD_UNCHANGED)
    
    # Convert both images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    symbol_gray = cv2.cvtColor(symbol, cv2.COLOR_BGR2GRAY)
    
    # Match the template using matchTemplate method
    result = cv2.matchTemplate(screenshot_gray, symbol_gray, cv2.TM_CCOEFF_NORMED)
    
    # Get the coordinates of the matched locations where the match value exceeds the threshold
    loc = np.where(result >= threshold)
    
    # Store the exact coordinates
    coordinates = []
    for pt in zip(*loc[::-1]):
        # Adjust coordinates to match the original screen
        adjusted_coordinates = (pt[0] + region[0], pt[1] + region[1])
        coordinates.append(adjusted_coordinates)
    
    return coordinates
        


def checkInv():
    global s1Full, s2Full, s3Full
    
    image_path = '.\\images\\' + IMAGE_FISH
    
    if (not s1Full):
        pyautogui.press(s1Key)
        time.sleep(generateRandomNumber(0.09, 0.13))
        pyautogui.click(button='right')
        last_slot = s1LastSlot
    elif (not s2Full):
        pyautogui.press(s2Key)
        time.sleep(generateRandomNumber(0.09, 0.13))
        pyautogui.click(button='right')
        last_slot = s2LastSlot
    elif (not s3Full):
        pyautogui.press(s3Key)
        time.sleep(generateRandomNumber(0.09, 0.13))
        pyautogui.click(button='right')
        last_slot = s3LastSlot
    else:
        return
    
    time.sleep(2)
    
    # Detect Fishes in INVENTORY
    pyautogui.moveTo(cursor_neutral) # move cursor out of the way
    region = sRegionInventory
    screenshot = take_screenshot(region)
    symbol_path = image_path
    coordinates = detect_symbols(sRegionInventory, screenshot, symbol_path)

    # Output the detected coordinates
    if coordinates:
        # print(f"Fishes found at the following coordinates: {coordinates}")
        pyautogui.keyDown('shift')
        for coord in coordinates:
            pyautogui.moveTo(coord)
            pyautogui.click()
            time.sleep(generateRandomNumber(0.1, 0.15))
        pyautogui.keyUp('shift')
    else:
        print("Fish not found.")
        
        
    # Detect Fish in the last slot of currently opened bucket
    pyautogui.moveTo(cursor_neutral) # move cursor out of the way
    region = last_slot
    screenshot = take_screenshot(region)
    coordinates = detect_symbols(region, screenshot, symbol_path)
    if coordinates:
        if last_slot == s1LastSlot:
            s1Full = True
        elif last_slot == s2LastSlot:
            s2Full = True
        elif last_slot == s3LastSlot:
            s3Full = True 
    
    pyautogui.press('esc')
    time.sleep(0.5)
    pyautogui.press(poleKey)
    
    pass
    

def main():
    """Main function of the MinecraftFisher."""
    print('Running...')

    # Get the window
    pt1, pt2 = getDesiredWindow()
    # Give user grace period of 3 seconds before starting game
    print('Starting minecraft fisher in three seconds...')
    time.sleep(3)
    
    start_time = time.time()
    
    # Set the reference red pixel value
    refPixVal = getRedPixVal(pt1,pt2)
    print('Ref Pix Val: {}'.format(refPixVal))
    
    checkInvIn = 23
    
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
            
            checkInvIn -= 1
            if checkInvIn == 0:
                checkInv()
                checkInvIn = 18
            
            # Right click again to start fishing once again
            print('Casting...')
            pyautogui.click(button='right')
            # Wait for fishing bob to resume its position
            time.sleep(3) 
            
            # If it is still casted
            currentRedVal = getRedPixVal(pt1,pt2)
            counter = 0
            while(currentRedVal < refPixVal * 0.7):
                print(f'Current red value: {currentRedVal}')
                print(f'Reference red value: {refPixVal}')
                if counter == 3:
                    if (s1Full and s2Full and s3Full): 
                        print('!!! CANNOT CAST !!!')
                        print('Inventory is Full. Exiting program.')
                        
                        
                        ##### TIMER #####
                        
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        hours, rem = divmod(elapsed_time, 3600)
                        minutes, seconds = divmod(rem, 60)
                        print(f"Time taken: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
                        
                        ##### TIMER ENDS #####
                        
                        
                        exit(0)
                    else:
                        checkInv()
                
                pyautogui.press('2')
                time.sleep(0.15)
                pyautogui.press('1')
                time.sleep(0.2)
                pyautogui.click(button='right')
                counter += 1
                time.sleep(3)
                currentRedVal = getRedPixVal(pt1,pt2)
                
            time.sleep(1)

        time.sleep(0.30)


if __name__ == '__main__':
    main()