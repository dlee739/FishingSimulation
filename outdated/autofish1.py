import pyautogui
import easyocr
import cv2
import numpy
import time

# Setup a phrase to match and a region of the screen to search
initPhrase = "Bobber thrown"
magicPhrase = "Fishing hook splashes"
screenRegion = (1575, 627, 1920, 993)

# Variables
catchCount = 0

# Instantiate the OCR object
readerEN = easyocr.Reader(["en"], gpu=True)
# readerKR = easyocr.Reader(["kr"], gpu=True)

# ________________________________________________

# Initial casting of a fishing pole
pyautogui.moveTo(960, 307)
pyautogui.click()
time.sleep(1)
pyautogui.click(button="right")

#while True:
while True:
    phraseFound = False
    
    # Grab the defined screen region and convert it to a format that is 
    # faster to process with OCR
    screenCapture = pyautogui.screenshot(region=screenRegion)
    ocrImage = cv2.cvtColor(numpy.array(screenCapture), cv2.COLOR_RGB2BGR)
    results = readerEN.readtext(ocrImage)
    
    # Check if the word is found in the results
    for result in results:
        text = result[1] # Extract the recognized text
        if magicPhrase.lower() in text.lower():
            
            
            # NOISE
            
            
            # We have a match, force the mouse to the Minecraft window then perform a right-click
            phraseFound = True
            catchCount += 1
            print("[AutoFish] Attempting to catch number: " + str(catchCount), end="\r")
            pyautogui.click(button="right")
            
            # PULLING ALGORITHM + NOISE
            
            break
        
    
    # Cast again if found
    if phraseFound:
        time.sleep(2.0)
        pyautogui.click(button="right")
        
    time.sleep(0.1)
        
    # Forced delay to allow a keyboard interrupt
    # cv2.waitKey(200)
    
            