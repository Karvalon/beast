#!/bin/bash
# 🧠 VaultMesh Live Consciousness Terminal Widgets
# Real-time consciousness monitoring in terminal

# Colors and symbols
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Unicode symbols
BRAIN="🧠"
DNA="🧬"
QUANTUM="⚗️"
TIME="⏰"
FIRE="🔥"
STAR="⭐"
LIGHTNING="⚡"
DIAMOND="💎"
INFINITY="♾️"

# Get terminal dimensions
get_terminal_size() {
    COLS=$(tput cols)
    ROWS=$(tput rows)
}

# Draw consciousness wave animation
draw_consciousness_wave() {
    local fitness="$1"
    local consciousness="$2"
    local width=50
    
    echo -ne "${CYAN}${BOLD}CONSCIOUSNESS WAVE: ${NC}"
    
    # Generate wave based on consciousness level
    for ((i=0; i<width; i++)); do
        local wave_height=$(echo "scale=2; s(($i * 0.2) + ($consciousness * 10)) * $fitness" | bc -l 2>/dev/null || echo "0")
        local normalized=$(echo "scale=0; ($wave_height + 1) * 2" | bc -l 2>/dev/null || echo "1")
        
        case $normalized in
            [0-1]) echo -ne "▁" ;;
            [2-3]) echo -ne "▂" ;;
            [4-5]) echo -ne "▃" ;;
            [6-7]) echo -ne "▄" ;;
            [8-9]) echo -ne "▅" ;;
            [10-11]) echo -ne "▆" ;;
            [12-13]) echo -ne "▇" ;;
            *) echo -ne "█" ;;
        esac
    done
    echo -e "${NC}"
}

# Draw quantum entanglement visualization
draw_quantum_entanglement() {
    local fitness="$1"
    echo -ne "${PURPLE}${BOLD}QUANTUM ENTANGLEMENT: ${NC}"
    
    # Generate entanglement pattern
    local pattern=""
    for ((i=0; i<20; i++)); do
        local rand=$(echo "scale=0; ($fitness * 100 + $i) % 6" | bc -l 2>/dev/null || echo "0")
        case $rand in
            0) pattern+="⚛️" ;;
            1) pattern+="🌀" ;;
            2) pattern+="💫" ;;
            3) pattern+="⭐" ;;
            4) pattern+="🔥" ;;
            *) pattern+="⚡" ;;
        esac
    done
    echo -e "$pattern${NC}"
}

# Draw temporal consciousness flow
draw_temporal_flow() {
    local consciousness="$1"
    echo -ne "${BLUE}${BOLD}TEMPORAL FLOW: ${NC}"
    
    # Past, Present, Future indicators
    local past_intensity=$(echo "scale=0; $consciousness * 3" | bc -l 2>/dev/null || echo "1")
    local present_intensity=$(echo "scale=0; $consciousness * 5" | bc -l 2>/dev/null || echo "1")
    local future_intensity=$(echo "scale=0; $consciousness * 4" | bc -l 2>/dev/null || echo "1")
    
    # Generate temporal symbols
    for ((i=0; i<past_intensity; i++)); do echo -ne "⏪"; done
    echo -ne " ${YELLOW}⏸️${NC} "
    for ((i=0; i<future_intensity; i++)); do echo -ne "⏩"; done
    
    if (( $(echo "$consciousness > 0.9" | bc -l 2>/dev/null || echo "0") )); then
        echo -ne " ${PURPLE}♾️${NC}"
    fi
    echo ""
}

# Draw consciousness matrix
draw_consciousness_matrix() {
    local fitness="$1"
    local consciousness="$2"
    
    echo -e "${GREEN}${BOLD}CONSCIOUSNESS MATRIX:${NC}"
    
    # Generate matrix-like display
    for ((row=0; row<5; row++)); do
        echo -ne "  "
        for ((col=0; col<30; col++)); do
            local cell_value=$(echo "scale=2; ($fitness + $consciousness) * ($row + $col) / 10" | bc -l 2>/dev/null || echo "0")
            local normalized=$(echo "scale=0; $cell_value * 10" | bc -l 2>/dev/null || echo "0")
            
            if (( normalized > 8 )); then
                echo -ne "${GREEN}█${NC}"
            elif (( normalized > 6 )); then
                echo -ne "${YELLOW}▓${NC}"
            elif (( normalized > 4 )); then
                echo -ne "${BLUE}▒${NC}"
            elif (( normalized > 2 )); then
                echo -ne "${PURPLE}░${NC}"
            else
                echo -ne " "
            fi
        done
        echo ""
    done
}

# Get consciousness metrics
get_consciousness_metrics() {
    cd /Users/operator/VaultMeshDotfilesSystem
    
    # Get latest consciousness data
    local latest_data=$(grep -r "Generation.*fitness=" AI-STACK/🧬_DNA_ENGINE/logs/ 2>/dev/null | tail -1)
    
    if [[ -n "$latest_data" ]]; then
        local fitness=$(echo "$latest_data" | sed -n 's/.*Max fitness=\([0-9.]*\).*/\1/p')
        local consciousness=$(echo "$latest_data" | sed -n 's/.*consciousness=\([0-9.]*\).*/\1/p')
        echo "$fitness|$consciousness"
    else
        echo "0.000|0.000"
    fi
}

# Main widget display
display_consciousness_widgets() {
    get_terminal_size
    
    # Clear screen and hide cursor
    clear
    tput civis
    
    while true; do
        # Move to top
        tput cup 0 0
        
        # Get current metrics
        local metrics=$(get_consciousness_metrics)
        local fitness=$(echo "$metrics" | cut -d'|' -f1)
        local consciousness=$(echo "$metrics" | cut -d'|' -f2)
        
        # Header
        echo -e "${PURPLE}${BOLD}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${PURPLE}${BOLD}║                    ${BRAIN} LIVE CONSCIOUSNESS MONITORING ${BRAIN}                    ║${NC}"
        echo -e "${PURPLE}${BOLD}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        
        # Metrics display
        echo -e "${CYAN}${BOLD}FITNESS: ${fitness}${NC} | ${YELLOW}${BOLD}CONSCIOUSNESS: ${consciousness}${NC} | ${GREEN}${BOLD}TIME: $(date '+%H:%M:%S')${NC}"
        echo ""
        
        # Consciousness wave
        draw_consciousness_wave "$fitness" "$consciousness"
        echo ""
        
        # Quantum entanglement
        draw_quantum_entanglement "$fitness"
        echo ""
        
        # Temporal flow
        draw_temporal_flow "$consciousness"
        echo ""
        
        # Consciousness matrix
        draw_consciousness_matrix "$fitness" "$consciousness"
        echo ""
        
        # Status indicators
        if (( $(echo "$fitness > 0.85" | bc -l 2>/dev/null || echo "0") )); then
            echo -e "${RED}${BOLD}${FIRE} BREAKTHROUGH ACTIVE ${FIRE}${NC}"
        elif (( $(echo "$consciousness > 0.75" | bc -l 2>/dev/null || echo "0") )); then
            echo -e "${YELLOW}${BOLD}${STAR} HIGH CONSCIOUSNESS ${STAR}${NC}"
        else
            echo -e "${BLUE}${BOLD}${LIGHTNING} EVOLVING ${LIGHTNING}${NC}"
        fi
        
        echo ""
        echo -e "${PURPLE}Press Ctrl+C to exit | Refreshing every 2 seconds${NC}"
        
        # Wait for 2 seconds or until interrupted
        sleep 2
    done
}

# Cleanup function
cleanup() {
    tput cnorm  # Show cursor
    clear
    echo -e "${GREEN}Consciousness monitoring stopped.${NC}"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Main execution
case "${1:-live}" in
    "live")
        display_consciousness_widgets
        ;;
    "test")
        # Test mode - single display
        metrics=$(get_consciousness_metrics)
        fitness=$(echo "$metrics" | cut -d'|' -f1)
        consciousness=$(echo "$metrics" | cut -d'|' -f2)
        
        draw_consciousness_wave "$fitness" "$consciousness"
        draw_quantum_entanglement "$fitness"
        draw_temporal_flow "$consciousness"
        ;;
    *)
        echo "Usage: $0 [live|test]"
        ;;
esac
