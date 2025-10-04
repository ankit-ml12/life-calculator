# Life Calculator

A minimal, lightweight life timer application for Kali Linux. Shows two side-by-side timers tracking elapsed time from February 14, 1999.

## Features

- **Dual Timer Display**: 80-year and 30-year timers side by side
- **Real-time Updates**: Shows years, months, days, hours, minutes, seconds
- **Minimal UI**: Clean, dark theme with green/orange text
- **Auto-start**: Launches automatically on system startup
- **Lightweight**: No external dependencies, uses built-in tkinter

## Quick Install

```bash
# Make installer executable and run
chmod +x install.sh
./install.sh
```

This will:
- Install the app to `~/.local/share/life-calculator/`
- Create desktop shortcut in applications menu
- Setup autostart for next login

## Manual Installation

```bash
# Run directly without installing
python3 src/main.py

# Or copy to desired location and update paths in desktop files
```

## Uninstall

```bash
./uninstall.sh
```

## Requirements

- Python 3 (pre-installed on Kali Linux)
- tkinter (included with Python)

## Usage

The app shows two timers:
- **Left**: 80-year timer (green text)
- **Right**: 30-year timer (orange text)

Both count elapsed time from February 14, 1999, updating every second.# life-calculator
