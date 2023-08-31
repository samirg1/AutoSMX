from setuptools import setup # type: ignore
import sys
from cx_Freeze import setup, Executable # type: ignore

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["pytest", "PyQt6", "PyQt5"],
    "packages": ["pyautogui", "pyperclip", "attrs", "pynput"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="guifoo",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/App.py", base=base)],
)

if __name__ == "__main__":
    setup()