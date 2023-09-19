@echo off
REM Pre-requisites:
REM install python 3
REM install
REM install git
@echo on

RMDIR /Q/S .venv
python -m venv .venv
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python3 -m pip install -e pyautogui
python3 -m pip install -e pillow
python3 -m pip install -e opencv-python
python3 -m pip install -e mss
