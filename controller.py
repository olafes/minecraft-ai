import ctypes
import win32api
import win32gui

PUL = ctypes.POINTER(ctypes.c_ulong)

keyboard_key_mapping = {
    'KEY_ESCAPE': 0x01,
    'KEY_1': 0x02,
    'KEY_2': 0x03,
    'KEY_3': 0x04,
    'KEY_4': 0x05,
    'KEY_5': 0x06,
    'KEY_6': 0x07,
    'KEY_7': 0x08,
    'KEY_8': 0x09,
    'KEY_9': 0x0A,
    'KEY_0': 0x0B,
    'KEY_W': 0x11,
    'KEY_S': 0x1F,
    'KEY_A': 0x1E,
    'KEY_D': 0x20,
    'KEY_E': 0x12,
    'KEY_LEFT_CTRL': 0x1D,
    'KEY_LEFT_SHIFT': 0x2A,
    'KEY_SPACE': 0x39,
}
mouse_button_down_mapping = {
    'LEFT': 0x0002,
    'RIGHT': 0x0008
}
mouse_button_up_mapping = {
    'LEFT': 0x0004,
    'RIGHT': 0x0010
}
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class Controller():
    def __init__(self, hwnd):
        self.hwnd = hwnd
    def press_key(self, key):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()

        flags = 0x0008
        key = keyboard_key_mapping[key]
        ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    def release_key(self, key):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()

        flags = 0x0008 | 0x0002
        key = keyboard_key_mapping[key]
        ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    def mouse_move(self, x, y, duration=0):
        # start_x, start_y = win32gui.ClientToScreen(hwnd, win32api.GetCursorPos())
        end_x, end_y = win32gui.ClientToScreen(self.hwnd, (x, y))

        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(end_x, end_y, 0, 0x0001, 0, ctypes.pointer(extra))

        command = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    def mouse_down(self, button='LEFT'):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, mouse_button_down_mapping[button], 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    def mouse_up(self, button='LEFT'):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, mouse_button_up_mapping[button], 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
