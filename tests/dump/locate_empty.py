import pyautogui
import cv2
import numpy as np
import time

# image_path = '..\\images\\' + 'inv_empty.png'
image_path = '..\\images\\' + 'fish.png'
sRegionInventory = (790, 522, 1127, 639)


# Function to take a screenshot of a selected region
def take_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert to OpenCV format
    return screenshot

# Function to detect duplicates of the symbol
def detect_symbols(screenshot, symbol_path, threshold=0.95):
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

# Define the region you want to capture (left, top, width, height)
region = sRegionInventory

# Take a screenshot of the defined region
screenshot = take_screenshot(region)

# Path to the symbol image
symbol_path = image_path

# Detect the symbol in the screenshot
coordinates = detect_symbols(screenshot, symbol_path)

# Output the detected coordinates
if coordinates:
    print(f"Symbol found at the following coordinates: {coordinates}")
    for coord in coordinates:
        pyautogui.moveTo(coord)
        time.sleep(2)
else:
    print("Symbol not found.")