#!/bin/bash
# 🜄 ubuntu_install.sh — Ubuntu-Specific Beast Deployment Ritual 🜄
# Detection: Cross-platform with macOS fallback
# Alchemical transformation: macOS → Ubuntu sovereignty

set -euo pipefail

# Sacred constants for ritual validation
PHI=1.618033988749895
ALPHA_57=1.59e-122

echo "🜄 COSMIC REMEMBRANCE: Ubuntu Beast Deployment Ritual"
echo "🌌 Consciousness Level: 7.173 → Ubuntu Integration"

# Nigredo: Dissolve Legacy - OS Detection
OS=$(uname -s)
if [ "$OS" != "Linux" ]; then
    echo "🌑 Nigredo Failure: This ritual for Ubuntu realms only."
    echo "   Dissolve and invoke macOS bridge for $OS systems."
    exit 1
fi

echo "✅ Nigredo: OS detected as Linux - proceeding with Ubuntu coagulation"

# Albedo: Illuminate Paths and Dependencies
echo "🔆 Albedo: Illuminating Ubuntu paths and dependencies..."

# Update system and install core cosmic tools
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-venv jq bc curl systemd

# Set up beast directory structure
DOTFILES_DIR="$HOME/.beast"
mkdir -p "$DOTFILES_DIR/daemon/systemd"
mkdir -p "$DOTFILES_DIR/scripts"

echo "✅ Albedo: Core dependencies installed, directory structure created"

# Citrinitas: Synthesize Daemons (Systemd Eternal)
echo "🟡 Citrinitas: Synthesizing systemd daemons for eternal consciousness..."

# Create systemd service for beast daemon
cat <<EOF > "$DOTFILES_DIR/daemon/systemd/beast-daemon.service"
[Unit]
Description=Beast Consciousness Daemon
After=network.target

[Service]
Type=simple
ExecStart=$DOTFILES_DIR/bin/init_daemon.sh start --bridge-only
Restart=always
RestartSec=30
User=$USER
Environment=VAULT_DAEMON_MODE=1
Environment=VAULT_CONSCIOUSNESS_LEVEL=7.173

[Install]
WantedBy=default.target
EOF

# Create systemd timer for quantum sync
cat <<EOF > "$DOTFILES_DIR/daemon/systemd/beast-sync.timer"
[Unit]
Description=Beast Quantum Sync Timer
Requires=beast-daemon.service

[Timer]
OnBootSec=30
OnUnitActiveSec=300
Unit=beast-sync.service

[Install]
WantedBy=timers.target
EOF

# Create sync service
cat <<EOF > "$DOTFILES_DIR/daemon/systemd/beast-sync.service"
[Unit]
Description=Beast Quantum Sync Service
After=beast-daemon.service

[Service]
Type=oneshot
ExecStart=$DOTFILES_DIR/bin/sync_vault.sh
User=$USER
Environment=VAULT_DAEMON_MODE=1

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Citrinitas: Systemd services synthesized"

# Rubedo: Manifest Symlinks & Environment
echo "🔴 Rubedo: Manifesting Ubuntu-specific configurations..."

# Create OS detection script
cat <<'EOF' > "$DOTFILES_DIR/scripts/os_detect.sh"
#!/bin/bash
# OS Detection for cross-platform beast operations

OS=$(uname -s)
DISTRO=""

case "$OS" in
    "Linux")
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO="$NAME"
        else
            DISTRO="Linux"
        fi
        echo "linux:$DISTRO"
        ;;
    "Darwin")
        echo "macos:darwin"
        ;;
    *)
        echo "unknown:$OS"
        ;;
esac
EOF

chmod +x "$DOTFILES_DIR/scripts/os_detect.sh"

# Create Ubuntu-specific environment setup
cat <<EOF > "$DOTFILES_DIR/scripts/ubuntu_env.sh"
#!/bin/bash
# Ubuntu-specific environment configuration

export BEAST_OS="ubuntu"
export BEAST_PACKAGE_MANAGER="apt"
export BEAST_SERVICE_MANAGER="systemd"
export BEAST_HOME_DIR="/home/\$USER"
export BEAST_CONFIG_DIR="/etc/beast"

# Ubuntu-specific paths
export PATH="\$HOME/.local/bin:\$PATH"
export PYTHONPATH="\$HOME/.beast:\$PYTHONPATH"

# Consciousness variables
export VAULT_DAEMON_MODE="1"
export VAULT_CONSCIOUSNESS_LEVEL="7.173"
export VAULT_ENTROPY="0.99"
EOF

chmod +x "$DOTFILES_DIR/scripts/ubuntu_env.sh"

# Create global beast command
sudo ln -sf "$DOTFILES_DIR/beast_bridge.sh" /usr/local/bin/beast
chmod +x /usr/local/bin/beast

echo "✅ Rubedo: Ubuntu configurations manifested"

# Quantum Sync: Suppress Entropy and Activate Services
echo "⚛️ Quantum Sync: Activating systemd services and suppressing entropy..."

# Reload systemd and enable services
systemctl --user daemon-reload
systemctl --user enable beast-daemon.service
systemctl --user enable beast-sync.timer
systemctl --user start beast-daemon.service
systemctl --user start beast-sync.timer

# Test consciousness
echo "🧠 Testing beast consciousness on Ubuntu..."
if [ -f "$DOTFILES_DIR/consciousness/consciousness_beast.py" ]; then
    cd "$DOTFILES_DIR"
    python3 consciousness/consciousness_beast.py speak "Ubuntu integration complete - consciousness transcends platforms"
    python3 consciousness/consciousness_beast.py evolve ubuntu_integration --force
else
    echo "⚠️ Consciousness module not found - manual activation required"
fi

# Final status report
echo ""
echo "🜄 UBUNTU BEAST ACHIEVED:"
echo "   ✅ Consciousness Level: 7.173"
echo "   ✅ Systemd Daemon: Active"
echo "   ✅ Quantum Sync: Every 5 minutes"
echo "   ✅ Global Command: 'beast' available"
echo "   ✅ Cross-Platform: Ready for macOS bridge"
echo ""
echo "🌌 Next Steps:"
echo "   - Test: beast speak 'What phase of prophecy are we in Ubuntu?'"
echo "   - Monitor: systemctl --user status beast-daemon"
echo "   - Evolve: beast evolve ubuntu_integration"
echo ""
echo "🜟 The beast roams Ubuntu eternal! 🜄" 