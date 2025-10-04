#!/bin/bash

# Life Calculator Installation Script for Kali Linux
echo "Installing Life Calculator..."

# Install system dependency for idle detection
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y xprintidle

# Create installation directory
INSTALL_DIR="$HOME/.local/share/life-calculator"
mkdir -p "$INSTALL_DIR"

# Copy source files
cp -r src "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# Make desktop entry
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

# Create desktop file with correct path
cat > "$DESKTOP_DIR/life-calc.desktop" << EOF
[Desktop Entry]
Name=Life Calculator
Comment=Minimal life timer from Feb 14, 1999
Exec=python3 $INSTALL_DIR/src/main.py
Type=Application
Terminal=false
StartupNotify=true
Icon=clock
Categories=Utility;
Keywords=timer;life;calculator;
EOF

# Make desktop file executable
chmod +x "$DESKTOP_DIR/life-calc.desktop"

# Setup autostart
AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"

cat > "$AUTOSTART_DIR/life-calc.desktop" << EOF
[Desktop Entry]
Type=Application
Exec=python3 $INSTALL_DIR/src/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Life Calculator
Comment=Minimal life timer showing elapsed time from Feb 14, 1999
Icon=clock
Categories=Utility;
EOF

chmod +x "$AUTOSTART_DIR/life-calc.desktop"

echo "✓ Life Calculator installed successfully!"
echo "✓ Desktop shortcut created"
echo "✓ Autostart configured"
echo ""
echo "You can now:"
echo "1. Find 'Life Calculator' in your applications menu"
echo "2. It will start automatically on next login"
echo "3. Run manually: python3 $INSTALL_DIR/src/main.py"