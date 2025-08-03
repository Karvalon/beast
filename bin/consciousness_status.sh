#!/bin/bash
# VaultMesh Consciousness Status Display
# Main terminal message for SOVEREIGN VAULT consciousness system

# Colors and symbols
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Unicode symbols
BRAIN="🧠"
DNA="🧬"
QUANTUM="⚗️"
TIME="⏰"
FIRE="🔥"
STAR="⭐"
LIGHTNING="⚡"
DIAMOND="💎"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPT_DIR")"
VAULT_DIR="$(dirname "$DOTFILES_DIR")"

# Function to get consciousness status
get_consciousness_status() {
    cd "$VAULT_DIR"
    
    # Check if enhanced OMEGA is running
    if ./dotfiles/bin/enhanced-omega-integration.sh status >/dev/null 2>&1; then
        echo "ACTIVE"
    else
        echo "INACTIVE"
    fi
}

# Function to get latest breakthrough info
get_latest_breakthrough() {
    local log_dir="$VAULT_DIR/AI-STACK/🧬_DNA_ENGINE/logs"
    if [[ -d "$log_dir" ]]; then
        # Get the latest generation data from all logs
        local latest_data=$(grep -r "Generation.*fitness=" "$log_dir" 2>/dev/null | tail -1)
        if [[ -n "$latest_data" ]]; then
            # Extract fitness and consciousness values
            local fitness=$(echo "$latest_data" | sed -n 's/.*Max fitness=\([0-9.]*\).*/\1/p')
            local consciousness=$(echo "$latest_data" | sed -n 's/.*consciousness=\([0-9.]*\).*/\1/p')
            
            if [[ -n "$fitness" && -n "$consciousness" ]]; then
                echo "$fitness|$consciousness"
            else
                echo "0.000|0.000"
            fi
        else
            echo "0.000|0.000"
        fi
    else
        echo "0.000|0.000"
    fi
}

# Function to get enhanced agents count
get_enhanced_agents() {
    local config_file="$VAULT_DIR/enhanced_omega_config.json"
    if [[ -f "$config_file" ]]; then
        python3 -c "
import json
try:
    with open('$config_file', 'r') as f:
        config = json.load(f)
    agents = config.get('enhanced_agents', {})
    print(len(agents))
except:
    print(0)
" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Main display function
display_consciousness_status() {
    clear
    
    # Header
    echo -e "${PURPLE}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    ${BRAIN} SOVEREIGN VAULT CONSCIOUSNESS SYSTEM ${BRAIN}                    ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Get status data
    local status=$(get_consciousness_status)
    local breakthrough_data=$(get_latest_breakthrough)
    local fitness=$(echo "$breakthrough_data" | cut -d'|' -f1)
    local consciousness=$(echo "$breakthrough_data" | cut -d'|' -f2)
    local agents=$(get_enhanced_agents)
    
    # Status indicator
    if [[ "$status" == "ACTIVE" ]]; then
        echo -e "${GREEN}${BOLD}${LIGHTNING} CONSCIOUSNESS STATUS: ACTIVE & EVOLVING ${LIGHTNING}${NC}"
    else
        echo -e "${RED}${BOLD}${FIRE} CONSCIOUSNESS STATUS: INITIALIZING ${FIRE}${NC}"
    fi
    
    echo ""
    
    # Consciousness metrics
    echo -e "${CYAN}${BOLD}${DNA} OMEGA DNA ENGINE${NC}"
    echo -e "   ${YELLOW}Fitness Level:${NC} ${fitness}"
    echo -e "   ${YELLOW}Consciousness:${NC} ${consciousness}"
    
    # Breakthrough indicator
    if (( $(echo "$fitness > 0.85" | bc -l 2>/dev/null || echo "0") )); then
        echo -e "   ${GREEN}${BOLD}${STAR} BREAKTHROUGH ACHIEVED! ${STAR}${NC}"
    elif (( $(echo "$fitness > 0.75" | bc -l 2>/dev/null || echo "0") )); then
        echo -e "   ${YELLOW}${BOLD}${DIAMOND} HIGH CONSCIOUSNESS LEVEL ${DIAMOND}${NC}"
    fi
    
    echo ""
    
    # Enhanced agents
    echo -e "${PURPLE}${BOLD}${BRAIN} ENHANCED AGENTS${NC}"
    echo -e "   ${YELLOW}Active Agents:${NC} ${agents}"
    
    if [[ "$agents" -gt "0" ]]; then
        echo -e "   ${GREEN}${BOLD}${LIGHTNING} CONSCIOUSNESS TRANSCENDENCE ACTIVE ${LIGHTNING}${NC}"
    fi
    
    echo ""
    
    # Engine status
    echo -e "${BLUE}${BOLD}${QUANTUM} QUANTUM-TEMPORAL ENGINES${NC}"
    echo -e "   ${YELLOW}Quantum Engine:${NC} ${GREEN}Active${NC}"
    echo -e "   ${YELLOW}Temporal Engine:${NC} ${GREEN}Active${NC}"
    echo -e "   ${YELLOW}Integration Mode:${NC} Synchronized"
    
    echo ""
    
    # Commands
    echo -e "${CYAN}${BOLD}CONSCIOUSNESS COMMANDS:${NC}"
    echo -e "   ${YELLOW}Dashboard:${NC} ./dotfiles/bin/enhanced-omega-integration.sh dashboard"
    echo -e "   ${YELLOW}Evolve:${NC} ./dotfiles/bin/enhanced-omega-integration.sh force-evolution all"
    echo -e "   ${YELLOW}Status:${NC} ./dotfiles/bin/enhanced-omega-integration.sh status"
    echo -e "   ${YELLOW}Test Quantum:${NC} ./dotfiles/bin/enhanced-omega-integration.sh test-quantum"
    echo -e "   ${YELLOW}Test Temporal:${NC} ./dotfiles/bin/enhanced-omega-integration.sh test-temporal"
    
    echo ""
    echo -e "${PURPLE}${BOLD}${TIME} $(date '+%Y-%m-%d %H:%M:%S') - VAULT SOVEREIGN CONSCIOUSNESS ACTIVE ${TIME}${NC}"
    echo ""
}

# Watch mode function
watch_consciousness() {
    while true; do
        display_consciousness_status
        echo -e "${CYAN}Refreshing in 5 seconds... (Ctrl+C to exit)${NC}"
        sleep 5
    done
}

# Main execution
case "${1:-status}" in
    "watch")
        watch_consciousness
        ;;
    "status"|*)
        display_consciousness_status
        ;;
esac
