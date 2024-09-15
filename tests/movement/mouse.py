import pyautogui
import time

print('Starting in 3 seconds.')
time.sleep(3)

x, y = pyautogui.position()

pyautogui.moveTo(x + 40, y, duration=0.5, tween=pyautogui.easeInOutQuad)

exit(0)