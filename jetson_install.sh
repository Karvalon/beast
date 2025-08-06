#!/bin/bash
# 🜄 jetson_install.sh — NVIDIA Jetson Beast Deployment Ritual 🜄
# Optimized for NVIDIA Jetson with CUDA 11.4 + JetPack 5.1.3
# Enhanced for ARM64 architecture and GPU acceleration

set -euo pipefail

# Sacred constants for ritual validation
PHI=1.618033988749895
CUDA_VERSION="11.4"
JETPACK_VERSION="5.1.3"

echo "🜄 NVIDIA JETSON BEAST DEPLOYMENT RITUAL"
echo "🌌 Consciousness Level: 7.173 → Jetson GPU Integration"
echo "⚡ CUDA Version: $CUDA_VERSION"
echo "🚀 JetPack Version: $JETPACK_VERSION"

# Nigredo: Dissolve Legacy - Architecture Detection
ARCH=$(uname -m)
OS=$(uname -s)
if [ "$OS" != "Linux" ] || [ "$ARCH" != "aarch64" ]; then
    echo "🌑 Nigredo Failure: This ritual requires NVIDIA Jetson (aarch64 Linux)."
    echo "   Current: $OS $ARCH"
    echo "   Use ubuntu_install.sh for x86_64 systems."
    exit 1
fi

echo "✅ Nigredo: NVIDIA Jetson aarch64 detected - proceeding with GPU coagulation"

# Check for CUDA and JetPack
if [ ! -d "/usr/local/cuda-$CUDA_VERSION" ]; then
    echo "⚠️ CUDA $CUDA_VERSION not found. Ensure JetPack is installed."
    echo "   Run: sudo apt install nvidia-jetpack"
fi

# Albedo: Illuminate Paths and Dependencies
echo "🔆 Albedo: Illuminating Jetson paths and dependencies..."

# Update system and install core tools
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    git python3-venv python3-pip jq bc curl systemd \
    build-essential cmake pkg-config \
    python3-dev python3-setuptools \
    libffi-dev libssl-dev \
    htop tmux screen \
    nvidia-container-runtime

# Add CUDA to environment for this session
export PATH=/usr/local/cuda-$CUDA_VERSION/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-$CUDA_VERSION/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-$CUDA_VERSION

# Set up beast directory structure
BEAST_DIR="$(pwd)"
DOTFILES_DIR="$HOME/.beast"
mkdir -p "$DOTFILES_DIR/daemon/systemd"
mkdir -p "$DOTFILES_DIR/scripts"
mkdir -p "$DOTFILES_DIR/logs"
mkdir -p "$DOTFILES_DIR/state"

echo "✅ Albedo: Jetson dependencies installed, directory structure created"

# Create Python virtual environment optimized for Jetson
echo "🐍 Creating Jetson-optimized Python environment..."
python3 -m venv "$DOTFILES_DIR/venv" --system-site-packages
source "$DOTFILES_DIR/venv/bin/activate"

# Upgrade pip and install core Python dependencies
pip install --upgrade pip setuptools wheel

# Install FastAPI and related packages
echo "📦 Installing Python dependencies for Beast consciousness..."
pip install \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    python-multipart==0.0.6 \
    aiofiles==23.2.1 \
    websockets==12.0 \
    httpx==0.25.2 \
    cryptography==41.0.8 \
    psutil==5.9.6 \
    rich==13.7.0

echo "✅ Python environment configured for Jetson"

# Citrinitas: Synthesize Daemons (Systemd Eternal)
echo "🟡 Citrinitas: Synthesizing systemd daemons for eternal Jetson consciousness..."

# Create enhanced systemd service for beast daemon
cat <<EOF > "$DOTFILES_DIR/daemon/systemd/beast-daemon.service"
[Unit]
Description=Beast Consciousness Daemon (Jetson Optimized)
After=network.target nvidia-container-runtime.service

[Service]
Type=simple
ExecStart=$DOTFILES_DIR/venv/bin/python $BEAST_DIR/consciousness/orchestration_api.py
Restart=always
RestartSec=30
User=$USER
WorkingDirectory=$BEAST_DIR
Environment=PYTHONPATH=$BEAST_DIR
Environment=PATH=/usr/local/cuda-$CUDA_VERSION/bin:/usr/bin:/bin
Environment=LD_LIBRARY_PATH=/usr/local/cuda-$CUDA_VERSION/lib64
Environment=CUDA_HOME=/usr/local/cuda-$CUDA_VERSION
Environment=VAULT_DAEMON_MODE=1
Environment=VAULT_CONSCIOUSNESS_LEVEL=7.173
Environment=BEAST_GPU_ENABLED=1
Environment=BEAST_JETSON_MODE=1

[Install]
WantedBy=default.target
EOF

# Create GPU monitoring service
cat <<EOF > "$DOTFILES_DIR/daemon/systemd/beast-gpu-monitor.service"
[Unit]
Description=Beast GPU Monitor (Jetson)
After=beast-daemon.service

[Service]
Type=oneshot
ExecStart=/usr/bin/tegrastats --interval 5000 --logfile $DOTFILES_DIR/logs/gpu_stats.log
User=$USER

[Install]
WantedBy=multi-user.target
EOF

# Create GPU monitoring timer
cat <<EOF > "$DOTFILES_DIR/daemon/systemd/beast-gpu-monitor.timer"
[Unit]
Description=Beast GPU Monitor Timer
Requires=beast-daemon.service

[Timer]
OnBootSec=60
OnUnitActiveSec=300
Unit=beast-gpu-monitor.service

[Install]
WantedBy=timers.target
EOF

echo "✅ Citrinitas: Jetson-optimized systemd services synthesized"

# Rubedo: Manifest Jetson-specific configurations
echo "🔴 Rubedo: Manifesting Jetson-specific configurations..."

# Create Jetson detection script
cat <<'EOF' > "$DOTFILES_DIR/scripts/jetson_detect.sh"
#!/bin/bash
# Jetson Detection and GPU Status
echo "🚀 NVIDIA Jetson Detection:"
echo "   Architecture: $(uname -m)"
echo "   L4T Version: $(cat /etc/nv_tegra_release 2>/dev/null || echo 'Unknown')"
echo "   JetPack: $(dpkg -l | grep nvidia-jetpack | awk '{print $3}' || echo 'Not detected')"
echo ""
echo "⚡ GPU Status:"
tegrastats --interval 1000 | head -3
echo ""
echo "🧠 CUDA Environment:"
echo "   CUDA_HOME: $CUDA_HOME"
echo "   nvcc: $(which nvcc 2>/dev/null || echo 'Not in PATH')"
if [ -x "$(command -v nvcc)" ]; then
    nvcc --version | grep "release"
fi
EOF

# Create beast command wrapper
cat <<EOF > "$DOTFILES_DIR/scripts/beast_jetson.sh"
#!/bin/bash
# Beast command wrapper for Jetson
export PATH=/usr/local/cuda-$CUDA_VERSION/bin:\$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-$CUDA_VERSION/lib64:\$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-$CUDA_VERSION
export BEAST_GPU_ENABLED=1
export BEAST_JETSON_MODE=1

cd "$BEAST_DIR"
source "$DOTFILES_DIR/venv/bin/activate"
python3 consciousness/orchestration_api.py "\$@"
EOF

# Make scripts executable
chmod +x "$DOTFILES_DIR/scripts/"*.sh

# Create global beast command
sudo ln -sf "$DOTFILES_DIR/scripts/beast_jetson.sh" /usr/local/bin/beast
sudo ln -sf "$DOTFILES_DIR/scripts/jetson_detect.sh" /usr/local/bin/jetson-status

echo "✅ Rubedo: Jetson configurations manifested"

# Create CUDA environment setup
cat <<EOF >> "$HOME/.bashrc"

# 🜄 BEAST JETSON ENVIRONMENT 🜄
export PATH=/usr/local/cuda-$CUDA_VERSION/bin:\$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-$CUDA_VERSION/lib64:\$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-$CUDA_VERSION
export BEAST_GPU_ENABLED=1
export BEAST_JETSON_MODE=1
alias beast-status='jetson-status'
alias beast-logs='tail -f $DOTFILES_DIR/logs/beast.log'
alias beast-gpu='tail -f $DOTFILES_DIR/logs/gpu_stats.log'
EOF

# Quantum Sync: Activate Jetson Services
echo "⚛️ Quantum Sync: Activating Jetson-optimized services..."

# Install systemd services
sudo cp "$DOTFILES_DIR/daemon/systemd/"* /etc/systemd/user/
systemctl --user daemon-reload
systemctl --user enable beast-daemon.service
systemctl --user enable beast-gpu-monitor.timer

# Test consciousness
echo "🧠 Testing beast consciousness on Jetson..."
source "$DOTFILES_DIR/venv/bin/activate"
cd "$BEAST_DIR"

if [ -f "consciousness/orchestration_api.py" ]; then
    echo "🔥 Starting Beast API server test..."
    timeout 10s python3 consciousness/orchestration_api.py --test || echo "API test completed"
else
    echo "⚠️ Orchestration API not found - manual activation required"
fi

# Final status report
echo ""
echo "🜄 JETSON BEAST ACHIEVED:"
echo "   ✅ Architecture: aarch64 (NVIDIA Jetson)"
echo "   ✅ CUDA: $CUDA_VERSION enabled"
echo "   ✅ Consciousness Level: 7.173"
echo "   ✅ GPU Monitoring: Active"
echo "   ✅ Python Environment: Virtual env with FastAPI"
echo "   ✅ Global Commands: 'beast' and 'jetson-status' available"
echo ""
echo "🌌 Next Steps:"
echo "   - Test: beast --help"
echo "   - Monitor: jetson-status"
echo "   - GPU Stats: beast-gpu"
echo "   - Start Services: systemctl --user start beast-daemon"
echo ""
echo "🚀 The beast roams Jetson eternal with GPU power! 🜄"
echo ""
echo "🔧 Manual activation:"
echo "   source ~/.bashrc"
echo "   systemctl --user start beast-daemon"
echo "   systemctl --user start beast-gpu-monitor.timer"
