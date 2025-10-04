#!/bin/bash

# Life Calculator Uninstall Script
echo "Uninstalling Life Calculator..."

# Remove installation directory
INSTALL_DIR="$HOME/.local/share/life-calculator"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ Removed application files"
fi

# Remove desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/life-calc.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "✓ Removed desktop shortcut"
fi

# Remove autostart entry
AUTOSTART_FILE="$HOME/.config/autostart/life-calc.desktop"
if [ -f "$AUTOSTART_FILE" ]; then
    rm "$AUTOSTART_FILE"
    echo "✓ Removed autostart entry"
fi

echo "Life Calculator uninstalled successfully!"