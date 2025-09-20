@echo off
cd C:\Users\User\Downloads\gps-map\gps_project
call .venv\Scripts\activate
python screenshots\screenshot_bot.py >> log.txt 2>&1