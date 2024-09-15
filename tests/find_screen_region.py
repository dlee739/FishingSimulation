import pyautogui
import keyboard

def get_screen_region():
    print("Move your mouse to the first point and press 's' to select the first corner.")
    keyboard.wait('s')
    first_point = pyautogui.position()
    print(f"First point selected at: {first_point}")

    print("Move your mouse to the second point and press 'e' to select the opposite corner.")
    keyboard.wait('e')
    second_point = pyautogui.position()
    print(f"Second point selected at: {second_point}")

    x1, y1 = first_point
    x2, y2 = second_point

    # Calculate the top-left and bottom-right corners
    top_left_x = min(x1, x2)
    top_left_y = min(y1, y2)
    bottom_right_x = max(x1, x2)
    bottom_right_y = max(y1, y2)

    print(f"Selected region - Top-left corner: ({top_left_x}, {top_left_y}), Bottom-right corner: ({bottom_right_x}, {bottom_right_y})")

    return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

if __name__ == "__main__":
    region = get_screen_region()
    print(f"Screen region selected: {region}")