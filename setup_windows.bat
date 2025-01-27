@echo off
REM Pre-requisites:
REM install python 3
@echo on

RMDIR /Q/S .venv
python -m venv .venv
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install pyautogui
python -m pip install pillow
python -m pip install opencv-python
python -m pip install mss
python -m pip install numpy
