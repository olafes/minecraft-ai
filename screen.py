from ctypes import windll
import win32gui
import win32ui
from ctypes.wintypes import HWND, DWORD
from PIL import Image
import ctypes
import numpy as np

class Screen():
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.size = None
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(HWND(self.hwnd), DWORD(DWMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect))
            self.size = (rect.right - rect.left, rect.bottom - rect.top)
        else:
            self.size = self.GetSize()

        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC  = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
    def grab(self):
        w, h = self.size
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(self.mfcDC, w, h)

        self.saveDC.SelectObject(saveBitMap)
        result = windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), 1)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        return np.array(Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1))
