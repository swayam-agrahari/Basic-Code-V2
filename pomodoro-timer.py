import time
import argparse
import subprocess
import sys
import platform

def notify(title, message):
    """Send desktop notification, Linux only for now (notify-send)."""
    system = platform.system()
    if system == "Linux":
        try:
            subprocess.run(['notify-send', title, message])
        except FileNotFoundError:
      
            pass
    elif system == "Darwin":  # macOS
        try:
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
        except Exception:
            pass
    elif system == "Windows":
        pass

def countdown(minutes, label):
    total_seconds = minutes * 60
    try:
        while total_seconds:
            mins, secs = divmod(total_seconds, 60)
            timer = f"{label} Time: {mins:02d}:{secs:02d}"
            print(timer, end='\r', flush=True)
            time.sleep(1)
            total_seconds -= 1
        print(f"{label} Time: 00:00          ")
    except KeyboardInterrupt:
        print("\nTimer interrupted. Exiting...")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Terminal Pomodoro Timer")
    parser.add_argument('--work', type=int, default=25, help='Work duration in minutes (default 25)')
    parser.add_argument('--break', type=int, default=5, help='Break duration in minutes (default 5)')
    args = parser.parse_args()

    print(f"Starting Pomodoro Timer: {args.work} min work / {args.break} min break")
    try:
        while True:
            # Work timer
            countdown(args.work, "Work")
            notify("Pomodoro Timer", "Work session ended. Time for a break!")
            print("Work session complete! Take a break.")

            # Break timer
            countdown(args.break, "Break")
            notify("Pomodoro Timer", "Break session ended. Time to work!")
            print("Break session complete! Get ready to work.")
    except KeyboardInterrupt:
        print("\nPomodoro timer stopped. Have a productive day!")
        sys.exit(0)

if __name__ == '__main__':
    main()
