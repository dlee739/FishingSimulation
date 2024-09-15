from config import *


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


def timer(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return hours, minutes, seconds


# Function to take a screenshot of a selected region
def take_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert to OpenCV format
    return screenshot


# Function to detect duplicates of the symbol
def detect_symbols(region, screenshot, symbol_path, threshold=0.99):
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


def generateRandomNumber(min, max):
    randomNumber = random.uniform(min, max)
    return round(randomNumber, 2)


def randomizedClickTime(cps):
    tolerance = cps / 20
    return generateRandomNumber(1 / (cps + tolerance) , 1 / (cps - tolerance))


def find(screen_region, image_path):
    screenshot = take_screenshot(screen_region)
    return detect_symbols(screen_region, screenshot, image_path)


# def cast():
#     for i in range(3): 
#         if find(SR_ROD, IMAGE_PATH + IMAGE_ROD):
#             pyautogui.click(button='right')
#             time.sleep(2)
#         else: # Casted
#             time.sleep(2)
#             return True
    
#     if find(SR_ROD, IMAGE_PATH + IMAGE_ROD):
#         return False
    
    
def organizeInventory(full_1, full_2, full_3):
    fish_path = IMAGE_PATH + IMAGE_FISH
    
    # Open unfull storage
    if not full_1:      # Storage 1 
        pyautogui.press(KEY_AQUARIUM)
        time.sleep(0.1)
        pyautogui.click(button='right')
        last_slot = SR_LAST_1
    elif not full_2:    # Storage 2
        pyautogui.press(KEY_ICEBOX)
        time.sleep(0.1)
        pyautogui.click(button='right')
        last_slot = SR_LAST_2
    elif not full_3:    # Storage 3
        pyautogui.press(KEY_BUCKET)
        time.sleep(0.1)
        pyautogui.click(button='right')
        last_slot = SR_LAST_3
    else:
        return full_1, full_2, full_3 # All storages are full => Inventory is completely full => Exit program
    
    time.sleep(2) # Wait for storage to open
    
    # Find Fishes in INVENTORY
    pyautogui.moveTo(POS_NEUTRAL) # move cursor out of the way
    coordinates = find(SR_INVENTORY, fish_path)
    if coordinates:
        pyautogui.keyDown('shift')
        for coord in coordinates:
            pyautogui.moveTo(coord)
            pyautogui.click()
            time.sleep(generateRandomNumber(0.08, 0.1))
        pyautogui.keyUp('shift')
    else:
        print("Failed to organize inventory: Fish not found.")
        
    # Detect Fish in the last slot of currently opened bucket
    pyautogui.moveTo(POS_NEUTRAL) # move cursor out of the way
    coordinates = find(last_slot, fish_path)
    if coordinates:
        if last_slot == SR_LAST_1:
            full_1 = True
        elif last_slot == SR_LAST_2:
            full_2 = True
        elif last_slot == SR_LAST_3:
            full_3 = True 
    
    pyautogui.press('esc')
    time.sleep(0.5)
    pyautogui.press(KEY_ROD)
    
    return full_1, full_2, full_3


def tugging_fail():
    while isTugging():
        if generateRandomNumber(0, 100) < 50:
            pyautogui.click()
        else:
            pyautogui.click(button="right")
        time.sleep(0.15)
    time.sleep(2)
        

def tugging_human_error():
    pass


def isTugging():
    r, g, b = pyautogui.pixel(POS_TUG_BAR_X, POS_TUG_BAR_Y)
    # print(f"r,g,b: {r}, {g}, {b}")
    if (r, g, b) == (85, 85, 85) or (r, g, b) == (85, 255, 85) or (r, g, b) == (170, 170, 170):
        # print("Tugging")
        return True
    # print("Not tugging")
    return False


def tugging():
    ### INIT ###
    wasLeft = False
    fail = False
    cps = CPS
    changesDirection = 0
    ############
    
    # < 5% of Failure
    if generateRandomNumber(0, 100) < 5:
        fail = True
        
    time.sleep(0.2)
    
    print(f"Tugging Initiated! Success: {not fail}")
    while isTugging():
        if fail is True: # FAIL
            tugging_fail()
            return
        
        # if changesDirection >= 6:
        #     chanceFail = 3 * ((changesDirection - 5) ** 2)
        #     if generateRandomNumber(0, 100) <= chanceFail:
        #         print(f"Fail Triggered. Direction Changes: {changesDirection}, FailChance = {chanceFail}.")
        #         fail = True
        
        r, g, b = pyautogui.pixel(POS_TUG_MINIGAME_X, POS_TUG_MINIGAME_Y)
        
        # Click Left or Right
        if (r, g, b) == (255, 170, 0): # Gold (Left-Click)
            # print("LEFT")
            if not wasLeft:
                if generateRandomNumber(0, 100) < 10: # HUMAN ERROR
                    # print("HUMAN ERROR")
                    pyautogui.click(button="right")  
                wasLeft = True
                changesDirection += 1
                cps = CPS
            else:    
                pyautogui.click()
                cps = CPS_CONSECUTIVE
            
        elif (r, g, b) == (85, 255, 255): # Aqua (Right-Click)
            # print("RIGHT")
            if wasLeft:
                if generateRandomNumber(0, 100) < 10: # HUMAN ERROR
                    # print("HUMAN ERROR")
                    pyautogui.click()
                wasLeft = False
                changesDirection += 1
                cps = CPS
            else:    
                pyautogui.click(button="right")    
                cps = CPS_CONSECUTIVE
        
        time.sleep(randomizedClickTime(cps)) 
        
        
def save_map():
    ss = ImageGrab.grab(bbox=SR_MAP)
    save_directory = r".\\images"
    filename = IMAGE_MAP
    screenshot_path = os.path.join(save_directory, filename)
    ss.save(screenshot_path)


def main():
    print("\n\n\n********* Minecraft Autofish - Version 3.0 *********\n")
    
    ### INIT ###
    full_1 = False
    full_2 = False
    full_3 = False
    refRod = False
    ############
    
    # Get the window
    pt1, pt2 = getDesiredWindow()
    # Give user grace period of 3 seconds before starting script
    print('Starting in three seconds...')
    time.sleep(3)
    
    save_map() # save currently empty map
    
    start_time = time.time() # record starting time of the script
    
    # Set the reference red pixel value
    refPixVal = getRedPixVal(pt1,pt2)
    print('Reference Pixel Value: {}'.format(refPixVal))
    
    # Main fishing loop
    while True:
        currentRedVal = getRedPixVal(pt1,pt2)
        if currentRedVal < refPixVal * 0.65: 
            # print(currentRedVal)
            # Right-click to reel-in fish
            pyautogui.click(button='right')
            time.sleep(0.2)
            
            # Tugging Phase Begins
            tugging()
            
            # Wait for fishing bob to resume its position
            time.sleep(1.5)
            
            # Right click again to start fishing once again
            print('Casting...')
            # if refRod is False:
            #     # Save the reference image of uncasted fishing rod
            #     ss = ImageGrab.grab(bbox=SR_ROD)
            #     save_directory = r".\\images"
            #     filename = "rod.png"
            #     screenshot_path = os.path.join(save_directory, filename)
            #     ss.save(screenshot_path)
                
            #     refRod = True
            
            pyautogui.press(KEY_AQUARIUM)
            pyautogui.press(KEY_ROD)    
            pyautogui.click(button="right")
            time.sleep(3) 
            
            
            currentRedVal = getRedPixVal(pt1,pt2)
            if(currentRedVal < refPixVal * 0.65):
                pyautogui.click(button="right")
                time.sleep(3)
                currentRedVal = getRedPixVal(pt1,pt2)
                if(currentRedVal < refPixVal * 0.65):
                    if full_1 and full_2 and full_3:
                        print('!!! CANNOT CAST !!!')
                        print('Inventory is Full: Ending Script.')
                        
                        # Time how long it took
                        hours, minutes, seconds = timer(start_time)
                        print(f"Time Taken: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
                        
                        # Additional Report
                        
                        exit(0)
                
                    full_1, full_2, full_3 = organizeInventory(full_1, full_2, full_3)
                    time.sleep(0.3)
                    pyautogui.click(button="right")
                    time.sleep(3)
                
            # MAP RADAR SCAN FOR NEARBY PLAYERS
            if find(SR_MAP, ".\\images\\map.png"):
                # print("No player detected.")
                pass
            else:
                print("Player detected!")
                winsound.Beep(2000, 8000)
                        
                
            # if cast() is not True:
            #     if full_1 and full_2 and full_3:
            #         print('!!! CANNOT CAST !!!')
            #         print('Inventory is Full: Ending Script.')
                    
            #         # Time how long it took
            #         hours, minutes, seconds = timer(start_time)
            #         print(f"Time Taken: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
                    
            #         # Additional Report
                    
            #         exit(0)
                
            #     full_1, full_2, full_3 = organizeInventory(full_1, full_2, full_3)
                
            # time.sleep(2)

        time.sleep(0.25)


if __name__ == '__main__':
    main()