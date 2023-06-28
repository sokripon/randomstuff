"""Intended to be used as a windows task-scheduler task to start Windows Terminal hidden,
to have the quake terminal available at any time. (Deprecated, using the powershell script instead))"""
try:
    import win32api

except ImportError:
    raise ImportError("win32api not found. Please install pywin32")

import subprocess


def is_process_running(process_name):
    output = subprocess.check_output(["tasklist"]).decode("utf-8")
    return process_name.lower() in output.lower()


def main():
    if is_process_running("WindowsTerminal.exe"):
        print("Windows Terminal is running, nothing to do")
    else:
        print("Windows Terminal is not running")
        win32api.ShellExecute(0, "open", "wt.exe", "", "/", 0)
        print("Windows Terminal is now running")


if __name__ == "__main__":
    main()
