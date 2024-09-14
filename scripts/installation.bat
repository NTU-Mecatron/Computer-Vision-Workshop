@echo off
REM Create a virtual environment
python3 -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install the required packages
pip install -r SDK\requirements.txt
