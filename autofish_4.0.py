from config import *

# HOURS:MINUTES:SECONDS
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


def find(screen_region, image_path, th=0.99):
    screenshot = take_screenshot(screen_region)
    return detect_symbols(screen_region, screenshot, image_path, threshold=th)


def cast():
    pass
    
    
def organizeInventory(full_1, full_2, full_3, full_4, full_5):
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
        
    elif not full_4:    # Storage 4
        pyautogui.press(KEY_HUGE)
        time.sleep(0.1)
        pyautogui.click(button='right')
        last_slot = SR_LAST_1
        
    elif not full_5:
        pyautogui.press(KEY_HUGE)
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        pyautogui.click(button='right')
        pyautogui.keyUp('shift')
        last_slot = SR_LAST_1
        
    else:
        return full_1, full_2, full_3, full_4, full_5 # All storages are full => Inventory is completely full => Exit program
    
    time.sleep(2) # Wait for storage to open
    
    # Find Fishes in INVENTORY
    pyautogui.moveTo(POS_NEUTRAL) # move cursor out of the way
    coordinates = find(SR_INVENTORY, fish_path, th=0.95)
    if coordinates:
        pyautogui.keyDown('shift')
        for coord in coordinates:
            pyautogui.moveTo(coord)
            pyautogui.click()
            time.sleep(generateRandomNumber(0.05, 0.08))
        pyautogui.keyUp('shift')
    else:
        print("Failed to organize inventory: Fish not found.")
        
    # Detect Fish in the last slot of currently opened bucket
    pyautogui.moveTo(POS_NEUTRAL) # move cursor out of the way
    coordinates = find(last_slot, fish_path, th=0.95)
    if coordinates:
        if last_slot == SR_LAST_1:
            if not full_1:
                full_1 = True
            elif not full_4:
                full_4 = True
            elif not full_5:
                full_5 = True
        elif last_slot == SR_LAST_2:
            full_2 = True
        elif last_slot == SR_LAST_3:
            full_3 = True 
    
    pyautogui.press('esc')
    time.sleep(0.5)
    pyautogui.press(KEY_ROD)
    
    if coordinates:
        return organizeInventory(full_1, full_2, full_3, full_4, full_5)
    return full_1, full_2, full_3, full_4, full_5


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
    if generateRandomNumber(0, 100) < CHANCE_INITIAL_FAIL:
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
                if generateRandomNumber(0, 100) < CHANCE_HUMAN_ERROR: # HUMAN ERROR
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
                if generateRandomNumber(0, 100) < CHANCE_HUMAN_ERROR: # HUMAN ERROR
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
    
    
def player_nearby():
    if RADAR_ALERT is False: # Alert is set to OFF
        print("[Tournament] Radar Alert System is set to OFF.")
        return False
    
    # MAP RADAR SCAN FOR NEARBY PLAYERS
    if find(SR_MAP, IMAGE_PATH + IMAGE_MAP): # No players nearby
        return False
    else:
        print("[WARNING] PLAYER DETECTED NEARBY!")
        print("[WARNING] PLAYER DETECTED NEARBY!")
        print("[WARNING] PLAYER DETECTED NEARBY!")
        winsound.Beep(2000, 4000)
        time.sleep(1)
        winsound.Beep(2000, 4000)
        return True
    
    
def rod_not_casting():
    r, g, b = pyautogui.pixel(POS_ROD_INVENTORY_X, POS_ROD_INVENTORY_Y)
    return (r, g, b) == (255, 255, 255)


def main():
    print("\n\n\n********* Minecraft Autofish - Version 4.0 *********\n")
    
    ### INIT ###
    full_1 = False
    full_2 = False
    full_3 = False
    full_4 = False
    full_5 = False
    sum_cast_durations = 0
    count_casts = 0
    sum_tug_durations = 0
    count_tugs = 0
    ############
    
    # Give user grace period of 3 seconds before starting script
    print('Starting in three seconds...')
    time.sleep(3)
    
    save_map() # save current map (supposedly containing no players nearby)
    print("Map Saved.")
    print("Script Started.")
    start_time = time.time() # record starting time of the script
    start_time_cast = time.time()
    
    # Main fishing loop
    while True:
        
        # Look for "Fishing hook splashes" subtitles (Fish is on the hook)
        fish_caught = find(SR_SUBTITLES, IMAGE_PATH + IMAGE_SUB_FISH, th=0.7) 
        if fish_caught:
            # print("Sub detected.")
            pyautogui.click(button="right")
            
            if DETAILED_REPORT:
                end_time_cast = time.time()
                cast_duration = round(end_time_cast - start_time_cast, 4)
                print(f"Cast ({count_casts + 1}) Duration: {cast_duration} seconds")
                
                count_casts += 1
                sum_cast_durations += cast_duration
                
            
            time.sleep(0.2)
            
            if DETAILED_REPORT:
                start_time_tug = time.time()
            
            # Tugging Phase Begins
            tugging()
            
            if DETAILED_REPORT:
                end_time_tug = time.time()
                tug_duration = round(end_time_tug - start_time_tug, 4)
                print(f"Tug ({count_tugs + 1}) Duration: {tug_duration} seconds")
                
                count_tugs += 1
                sum_tug_durations += tug_duration
            
            # Wait for fishing bob to resume its position
            time.sleep(1)
            
            if player_nearby():
                print("Detected presence of other players. Prematurely ending the script.")
                pyautogui.press(KEY_AQUARIUM)
                exit(0)
                
            counter_cast = 0
            print('Casting...')
            # while find(SR_ROD_INVENTORY, IMAGE_PATH + IMAGE_ROD_BEFORE, th=0.7): # While Rod is at initial state (not casted)
            
            while rod_not_casting():
                if counter_cast == 2:
                    if full_1 and full_2 and full_3 and full_4 and full_5: 
                        print('!!! CANNOT CAST !!!')
                        print('!!! CANNOT CAST !!!')
                        print('!!! CANNOT CAST !!!')
                        print('Inventory is Full: Ending Script.')
                        
                        winsound.Beep(2000, 5000)
                        
                        # Time how long it took
                        hours, minutes, seconds = timer(start_time)
                        print(f"[REPORT] Time Taken: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
                        
                        # Additional Report
                        if DETAILED_REPORT:
                            # Cast Info
                            avg_cast_duration = round(sum_cast_durations / count_casts, 4)
                            print(f"[REPORT] Total Casts & Reels: {count_casts}")
                            print(f"[REPORT] Average Cast Duration: {avg_cast_duration} seconds")
                            
                            # Tug Info
                            avg_tug_duration = round(sum_tug_durations / count_tugs, 4)
                            print(f"[REPORT] Average Tug Duration: {avg_tug_duration} seconds")
                        
                        exit(0)
                        
                    full_1, full_2, full_3, full_4, full_5 = organizeInventory(full_1, full_2, full_3, full_4, full_5)
                    time.sleep(0.3)
                elif counter_cast > 2:
                    print("CANNOT FIND CASTED ROD.")
                    
                    winsound.Beep(2000, 2000)
                    time.sleep(1)
                    winsound.Beep(2000, 2000)
                    time.sleep(1)
                    winsound.Beep(2000, 2000)
                    time.sleep(1)
                    
                    exit(0)
                    
                # Right click again to start fishing once again
                pyautogui.click(button="right")
                counter_cast += 1
                time.sleep(1)
            
            if DETAILED_REPORT:
                start_time_cast = time.time()
            
                
        time.sleep(0.20)
        
if __name__ == '__main__':
    main()