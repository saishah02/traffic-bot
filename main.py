import threading
import os
import sys
from django.core.management import execute_from_command_line

# Import bot logic
try:
    from gps_project.screenshot_bot import run_bot  # ubah kalau bot.py ada nama lain
except ImportError:
    print("Bot module not found. Skipping bot startup.")

# Start bot in background thread
def start_bot():
    try:
        run_bot()
    except Exception as e:
        print(f"Bot crashed: {e}")

threading.Thread(target=start_bot, daemon=True).start()

# Start Django server
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gps_project.settings")
execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])