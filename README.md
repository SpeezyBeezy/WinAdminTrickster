# WinAdminTrickster
Muwahaha trick your windows system admistrator into giving you (a standard user) permanat admin (work in progress purely made by ai)
Got the clanker who made it to write out a readme file I typing out all that go figure

***
A lightweight Windows service that allows you to run programs with administrator privileges via right-click context menu, without UAC prompts.

## ⚠️ Requirements

- **Windows Vista or later** (UAC required)
- **Python 3.6+**
- **Administrator access** (needed once for setup)

## 📦 Installation

### Step 1: Install Python

Install Python from the **Microsoft Store** (no admin required):
1. Open Microsoft Store
2. Search for "Python"
3. Install the latest version
4. Python will automatically be added to PATH

### Step 2: Verify Python Installation

Open Command Prompt and run:
```cmd
python --version
```

If you see a version number, you're good to go!

### Step 3: Download elv

1. Download this repository as ZIP
2. Extract to any folder
3. Make sure `nssm.exe` is in the same folder as `setup.py`

### Step 4: Run Setup

**Important:** Right-click `setup.py` → **Open with** → Select your Python installation

Or from Command Prompt:
```cmd
python setup.py
```

The setup will:
- Install required dependencies (pywin32)
- Copy files to `C:\Users\Public\Documents\elv`
- Install the Windows service
- Add context menu entry

## Usage

After installation:

1. Right-click any file or executable
2. Click **"elv"** from the context menu
3. The program launches with administrator privileges!

No UAC prompts, no hassle.

## How It Works

1. **Service runs at startup** with SYSTEM privileges
2. **Elevator process** runs hidden in the background with admin rights
3. **Context menu** creates a request file when you right-click → elv
4. **Elevator watches** the request queue folder
5. **Launches your program** elevated and cleans up the request

```
User right-clicks file
    ↓
context_menu.py creates request.json
    ↓
elevator.py detects new request
    ↓
Launches program with admin privileges
    ↓
Deletes request.json
```

## 🗑️ Uninstall

Run `uninstall.py` with administrator privileges:
```cmd
python uninstall.py
```

This removes:
- The Windows service
- Context menu entry
- All installed files

## 📁 File Structure

```
elv/
├── setup.py           # Installation script
├── uninstall.py       # Removal script
├── service.py         # Windows service
├── elevator.py        # Elevation handler
├── context_menu.py    # Context menu integration
└── nssm.exe          # Service wrapper
```

## ⚙️ Troubleshooting

**Service won't start:**
- Make sure you have administrator privileges
- Check Windows Event Viewer for errors
- Verify pywin32 is installed: `pip list | findstr pywin32`

**Context menu doesn't appear:**
- Restart Windows Explorer (Task Manager → Restart)
- Run `setup.py` again as administrator

**Programs don't launch elevated:**
- Check if the service is running: `nssm status ElevationService`
- Verify files exist in: `C:\Users\Public\Documents\elv`

**Python not found error:**
- Make sure Python is in PATH
- Try using full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\python.exe setup.py`


## 📝 License

MIT License - Use at your own risk (whatever that is)

## 🤝 Contributing

Issues and pull requests welcome! (I got no idea what I'm doing soo)

---
