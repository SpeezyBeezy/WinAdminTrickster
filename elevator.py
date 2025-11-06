import os
import json
import subprocess
import sys
import time
from datetime import datetime

QUEUE_DIR = r"C:\Users\Public\Documents\elv\queue"

# Create queue directory if not exists
os.makedirs(QUEUE_DIR, exist_ok=True)

while True:
    try:
        # Check for .json files in queue
        for filename in os.listdir(QUEUE_DIR):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(QUEUE_DIR, filename)
            
            try:
                # Read request
                with open(filepath, 'r') as f:
                    request = json.load(f)
                
                path = request.get('path', '')
                args = request.get('args', [])
                
                if not path or not os.path.exists(path):
                    os.remove(filepath)
                    continue
                
                # Launch process
                _, ext = os.path.splitext(path)
                if ext.lower() == '.py':
                    cmd = [sys.executable, path] + args
                else:
                    cmd = [path] + args
                
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                
                # Delete request file after launching
                os.remove(filepath)
                
            except Exception as e:
                # Delete bad request
                try:
                    os.remove(filepath)
                except:
                    pass
        
        time.sleep(0.5)
        
    except Exception as e:
        time.sleep(1)