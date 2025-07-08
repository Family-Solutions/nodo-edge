@echo off
echo Testing API Synchronization (Single Cycle)...
echo.

cd /d "f:\Github\nodo-edge"
"C:/Users/pc/AppData/Local/Programs/Python/Python312/python.exe" sync-api.py --test

echo.
echo Test completed. Press any key to exit...
pause
