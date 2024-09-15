from config import *
import Fishing.outdated.autofishV3 as autofishV3

SR_MAP = (1665, 67, 1865, 277)

# Function to take a screenshot of the minimap region
def take_screenshot():
    return pyautogui.screenshot(region=SR_MAP)

# Function to compare two images
def images_are_different(img1, img2, threshold=50):
    # Calculate the difference between the images
    diff = ImageChops.difference(img1, img2)
    
    # Convert the difference to grayscale
    diff = diff.convert('L')
    
    # Convert the difference to a numpy array and sum the differences
    diff_np = np.array(diff)
    diff_sum = np.sum(diff_np)
    
    print(f"diff sum: {diff_sum}")
    
    # Return True if the difference exceeds the threshold
    return diff_sum > threshold

# Wait for the user to press 'P' to take the initial screenshot
print("Press ']' to capture the initial map screenshot.")
keyboard.wait(']')
# original_screenshot = take_screenshot()

ss = ImageGrab.grab(bbox=SR_MAP)
save_directory = r".\\images"
filename = "map.png"
screenshot_path = os.path.join(save_directory, filename)
ss.save(screenshot_path)


print("Initial screenshot captured.")

# Main loop to scan the minimap every 5 seconds
while True:
    keyboard.wait(']')
    new_screenshot = take_screenshot()
    
    # Compare it with the original screenshot
    if autofishV3.find(SR_MAP, ".\\images\\map.png"):
        print("No player detected.")
        
    else:
        print("Player detected!")
        winsound.Beep(2000, 10000)
        # playsound("alarm.mp3")  # Replace with the actual path to the alarm sound
        


