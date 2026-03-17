@echo off
cd /d "%~dp0"
python scripts\maintenance\healthcheck.py --gui
