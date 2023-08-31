import sys

from cx_Freeze import Executable, setup  # type: ignore

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["pytest", "PyQt6", "PyQt5", "cv2", "numpy", "mypy"],
    "packages": ["pyautogui", "pyperclip", "attrs", "pynput"],
    "include_msvcr": True,
    "include_files": "src/storage/store.json",
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="ALTER SMX Tool",
    version="1.0",
    description="GUI helper application for ALTER's SMX software",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/App.py", base=base, target_name="ALTER SMX Tool")],
)
