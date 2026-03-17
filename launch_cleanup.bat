@echo off
cd /d "%~dp0"
python scripts\maintenance\cleanup_workspace.py --gui
