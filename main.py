import win32gui
from controller import Controller
from screen import Screen
from PIL import ImageGrab, Image
import cv2
import time

def main():
    hwnd = win32gui.FindWindow(None, 'Minecraft 1.14.4')
    controller = Controller(hwnd)
    screen = Screen(hwnd)
    win32gui.SetForegroundWindow(hwnd)

    while True:
        cv2.imshow('window', screen.grab())
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    # time.sleep(3)
    # controller.press_key('KEY_W')
    # controller.mouse_down()
    # controller.mouse_move(300, 0)
    # time.sleep(5)
    # controller.mouse_up()
    # # while True:

if __name__ == '__main__':
    main()
