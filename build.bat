.\venv\Scripts\pyinstaller.exe -F -w main.py
xcopy .\vlc-3.0.16\ .\dist\RTMP_Capture\vlc-3.0.16\ /s/y/q
copy config.ini .\dist\RTMP_Capture\config.ini
copy .\dist\main.exe .\dist\RTMP_Capture\main.exe