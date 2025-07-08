@echo off
echo Starting API Synchronization Service...
echo.
echo This will sync data between APIs every 20 seconds:
echo 1. External API -> Local Database
echo 2. Local Database -> Collar API
echo.
echo To stop the service, press Ctrl+C
echo.

cd /d "f:\Github\nodo-edge"
"C:/Users/pc/AppData/Local/Programs/Python/Python312/python.exe" sync-api.py

pause
