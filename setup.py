import sys

from cx_Freeze import Executable, setup  # type: ignore

build_exe = {
    "excludes": ["pytest", "PyQt6", "PyQt5", "cv2", "numpy", "mypy", "test", "email", "pydoc_data", "multiprocessing", "rubicon"],
    "packages": ["pyautogui", "pyperclip", "attrs", "pynput"],
    "include_msvcr": True,
    "include_files": ["autosmx.png"],
}

bdist_mac = {"iconfile": "autosmx.ico", "bundle_name": "AutoSMX"}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="AutoSMX",
    version="1.0.0",
    description="GUI Automater for SMX",
    author="Samir Gupta",
    options={"build_exe": build_exe, "bdist_mac": bdist_mac},
    executables=[Executable("src/App.py", base=base, target_name="AutoSMX", icon="autosmx.ico")],
)
