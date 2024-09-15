import pyautogui
import numpy as np
import cv2
import time
from PIL import ImageGrab
import os

SR_ROD = (1310, 534, 1651, 1027)        # Fishing Rod While Handheld 
POS_NEUTRAL = (31, 44)                  # To move the cursor out of the way

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


def find(screen_region, image_path):
    #pyautogui.moveTo(POS_NEUTRAL) # move cursor out of the way
    screenshot = take_screenshot(screen_region)
    return detect_symbols(screen_region, screenshot, image_path)


def cast():
    print("Casting")
    for i in range(3): 
        print(f"Loop: {i}")
        if find(SR_ROD, '..\\images\\rod.png'):
            print("MATCH FOUND! NOT CASTED")
            pyautogui.click(button='right')
            time.sleep(2)
        else: # Casted
            print("Match not found...")
            return True
    
    if find(SR_ROD, '..\\images\\rod.png'):
        print("? FAILSAFE?")
        return False
    

print("Get Ready in 5 seconds...")
time.sleep(5)

print("Taking a screenshot.")
ss = ImageGrab.grab(bbox=SR_ROD)
save_directory = r"..\\images"
filename = "rod.png"
screenshot_path = os.path.join(save_directory, filename)
ss.save(screenshot_path)
print("Saved rod.png")
    
if cast():
    print("True")
else:
    print("False")