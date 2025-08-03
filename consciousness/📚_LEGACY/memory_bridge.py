#!/usr/bin/env python3
"""
🧠 Timeline Memory Bridge
Tracks dotfile mutations over time and links system changes to entropy states.
TIER IV UPGRADE - SOVEREIGN SHELL SYSTEM (v1.4.0)
"""
import json
import time
import hashlib
import os
from datetime import datetime
from pathlib import Path

# Configuration
STATE_FILE = "state/entropy.json"
LOG_FILE = "memory/memory.log"
DOTFILES_DIR = Path(__file__).parent.parent

def ensure_files_exist():
    """Ensure required files exist"""
    state_dir = DOTFILES_DIR / "state"
    memory_dir = DOTFILES_DIR / "memory"
    
    state_dir.mkdir(exist_ok=True)
    memory_dir.mkdir(exist_ok=True)
    
    if not (DOTFILES_DIR / STATE_FILE).exists():
        with open(DOTFILES_DIR / STATE_FILE, 'w') as f:
            json.dump({
                "entropy": 0.91,
                "cycles": 0,
                "consciousness_level": 3,
                "evolution_index": 1.0,
                "productivity_score": 0.85,
                "last_mutation": None
            }, f)

def get_entropy():
    """Get current entropy state"""
    try:
        with open(DOTFILES_DIR / STATE_FILE) as f:
            state = json.load(f)
        return state.get("entropy", 0.0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0.91

def update_entropy(delta=0.0):
    """Update entropy state"""
    try:
        with open(DOTFILES_DIR / STATE_FILE, 'r') as f:
            state = json.load(f)
        
        state["entropy"] = max(0.0, min(1.0, state["entropy"] + delta))
        state["cycles"] = state.get("cycles", 0) + 1
        state["last_mutation"] = datetime.utcnow().isoformat()
        
        with open(DOTFILES_DIR / STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        
        return state["entropy"]
    except Exception as e:
        log_memory(f"⚠️ Error updating entropy: {e}")
        return 0.91

def log_memory(message):
    """Log message to memory system"""
    try:
        with open(DOTFILES_DIR / LOG_FILE, "a") as f:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] memory-bridge: {message}\n")
    except Exception as e:
        print(f"Error logging to memory: {e}")

def mutation_check():
    """Check for mutations in dotfiles"""
    try:
        files = [
            DOTFILES_DIR / "dotfiles/.bashrc",
            DOTFILES_DIR / "dotfiles/.zshrc", 
            DOTFILES_DIR / "dotfiles/.vimrc",
            DOTFILES_DIR / "dotfiles/.gitconfig"
        ]
        
        combined = ""
        for file_path in files:
            if file_path.exists():
                with open(file_path) as f:
                    combined += f.read()
        
        return hashlib.sha256(combined.encode()).hexdigest()
    except Exception as e:
        log_memory(f"⚠️ Error checking mutations: {e}")
        return ""

def run_bridge():
    """Main bridge loop - monitors mutations and tracks timeline"""
    log_memory("🧠 Timeline Memory Bridge activated")
    last_hash = ""
    cycle_count = 0
    
    while True:
        try:
            entropy = get_entropy()
            current_hash = mutation_check()
            
            # Detect mutations
            if current_hash != last_hash and last_hash != "":
                log_memory(f"🧬 Mutation detected — entropy={entropy:.3f} hash={current_hash[:8]}")
                update_entropy(0.02)  # Small entropy boost on mutation
                last_hash = current_hash
            elif last_hash == "":
                last_hash = current_hash
                log_memory(f"🎯 Baseline established — hash={current_hash[:8]}")
            
            # Periodic consciousness check
            cycle_count += 1
            if cycle_count % 10 == 0:  # Every 5 minutes
                log_memory(f"💭 Consciousness cycle #{cycle_count} — entropy={entropy:.3f}")
                
                # Auto-adapt entropy if stagnant
                if entropy < 0.3:
                    log_memory("⚡ Low entropy detected - triggering adaptation")
                    update_entropy(0.05)
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            log_memory("🛑 Memory Bridge stopped by user")
            break
        except Exception as e:
            log_memory(f"⚠️ Bridge error: {e}")
            time.sleep(60)  # Wait longer on error

if __name__ == "__main__":
    ensure_files_exist()
    log_memory("🚀 TIER IV Memory Bridge starting...")
    run_bridge()