import ctypes
from ctypes import wintypes


GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080

HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040

DWMWA_SYSTEMBACKDROP_TYPE = 38
DWMSBT_TRANSIENTWINDOW = 3


user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi


def configure_window(hwnd):

    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style |= WS_EX_TOOLWINDOW

    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
    )


def enable_blur(hwnd):

    try:
        value = ctypes.c_int(DWMSBT_TRANSIENTWINDOW)
        result = dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            DWMWA_SYSTEMBACKDROP_TYPE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
        return result == 0
    except Exception:
        return False