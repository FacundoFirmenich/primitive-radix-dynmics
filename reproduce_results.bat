@echo off
python -m pip install -e .[dev]
if errorlevel 1 exit /b 1
make reproduce
