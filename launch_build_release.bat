@echo off
cd /d "%~dp0"
python scripts\release\build_release_zip.py --gui
