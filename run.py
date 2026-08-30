import os
import subprocess

# Automatically install required packages if missing
subprocess.run(["pip", "install", "-r", "requirements.txt"])

# Run your main bot file
os.system("python3 bot.py")
