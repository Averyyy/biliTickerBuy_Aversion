import pyautogui
import time

# Replace x, y with the coordinates of the Colab avatar on your screen
x = -1955
y = 1130

while True:
    pyautogui.click(x, y)
    time.sleep(2)
    pyautogui.click(x, y)
    time.sleep(1)  # 5 minutes in seconds
    