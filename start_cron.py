import os, subprocess, sys, time

def start_scheduler():
    # starts daily_alerts.py in the background
    return subprocess.Popen([sys.executable, "daily_alerts.py"])

if __name__ == "__main__":
    proc = start_scheduler()
    print("Scheduler started with PID", proc.pid)
    try:
        # keep the Render container alive
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        proc.terminate()
        print("Scheduler stopped.")