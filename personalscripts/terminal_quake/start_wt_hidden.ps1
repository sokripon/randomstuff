# Intended to be used as a Windows Task Scheduler task to start the Windows Terminal hidden when Windows starts, making the quake terminal available at any time.
Start-Process -FilePath "wt.exe" -WindowStyle Hidden
#powershell -Command Start-Process -FilePath "wt.exe" -WindowStyle Hidden