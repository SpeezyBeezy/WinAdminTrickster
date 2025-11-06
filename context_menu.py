import sys
import json
import os
from datetime import datetime

QUEUE_DIR = r"C:\Users\Public\Documents\elv\queue"

if len(sys.argv) < 2:
    sys.exit(1)

# Get file path from argument
path = sys.argv[1]
args = sys.argv[2:] if len(sys.argv) > 2 else []

# Create queue directory if not exists
os.makedirs(QUEUE_DIR, exist_ok=True)

# Create request file with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
request_file = os.path.join(QUEUE_DIR, f"{timestamp}.json")

request = {
    "path": path,
    "args": args
}

with open(request_file, 'w') as f:
    json.dump(request, f)