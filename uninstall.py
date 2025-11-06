import subprocess
import sys
import ctypes
import os
import shutil
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

elv_dir = r"C:\Users\Public\Documents\elv"
script_dir = os.path.dirname(os.path.abspath(__file__))

print("Uninstalling elv...")

# Stop and remove service
nssm = os.path.join(script_dir, "nssm.exe")
if not os.path.exists(nssm):
    nssm = os.path.join(elv_dir, "nssm.exe")

if os.path.exists(nssm):
    print("Removing service...")
    subprocess.run([nssm, "stop", "ElevationService"], check=False)
    subprocess.run([nssm, "remove", "ElevationService", "confirm"], check=False)

# Remove context menu
print("Removing context menu...")
try:
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\elv\command")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\elv")
except:
    pass

# Delete elv directory
print("Deleting files...")
try:
    shutil.rmtree(elv_dir)
except:
    pass

print("\n✓ Uninstall complete!")
input("Press Enter to exit...")