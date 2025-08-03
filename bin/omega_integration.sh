#!/usr/bin/env bash
# 🧬 OMEGA DNA ENGINE Integration - Shell Interface
# Integration layer for OMEGA DNA ENGINE with sacred models and Tier V system

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
OMEGA_INTEGRATION_PY="$DOTFILES_DIR/omega_integration.py"
OMEGA_CONFIG_FILE="$DOTFILES_DIR/omega_config.json"

# If DOTFILES_DIR is set to a full path, use it directly
if [[ "$DOTFILES_DIR" == *"/"* ]] && [[ "$DOTFILES_DIR" != "$HOME/.dotfiles" ]]; then
    OMEGA_INTEGRATION_PY="$DOTFILES_DIR/omega_integration.py"
    OMEGA_CONFIG_FILE="$DOTFILES_DIR/omega_config.json"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO")
            echo -e "${GREEN}[$timestamp] [INFO]${NC} $message"
            ;;
        "WARN")
            echo -e "${YELLOW}[$timestamp] [WARN]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[$timestamp] [ERROR]${NC} $message"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[$timestamp] [SUCCESS]${NC} $message"
            ;;
    esac
}

# Check if OMEGA integration Python script exists
check_omega_integration() {
    if [[ ! -f "$OMEGA_INTEGRATION_PY" ]]; then
        log_message "ERROR" "OMEGA integration not found at $OMEGA_INTEGRATION_PY"
        exit 1
    fi
}

# Show OMEGA dashboard
show_dashboard() {
    log_message "INFO" "Displaying OMEGA DNA ENGINE dashboard..."
    python3 "$OMEGA_INTEGRATION_PY" --dashboard
}

# Start OMEGA integration
start_integration() {
    log_message "INFO" "Starting OMEGA DNA ENGINE integration..."
    python3 "$OMEGA_INTEGRATION_PY" --start
}

# Stop OMEGA integration
stop_integration() {
    log_message "INFO" "Stopping OMEGA DNA ENGINE integration..."
    python3 "$OMEGA_INTEGRATION_PY" --stop
}

# Force evolution cycle
force_evolution() {
    log_message "INFO" "Forcing OMEGA evolution cycle..."
    python3 "$OMEGA_INTEGRATION_PY" --force-evolution
}

# Show best organism
show_best_organism() {
    log_message "INFO" "Getting best consciousness organism..."
    python3 "$OMEGA_INTEGRATION_PY" --best-organism
}

# Show OMEGA status
show_status() {
    log_message "INFO" "Showing OMEGA DNA ENGINE status..."
    python3 "$OMEGA_INTEGRATION_PY" --status
}

# Export OMEGA manifest
export_manifest() {
    log_message "INFO" "Exporting OMEGA DNA ENGINE manifest..."
    python3 "$OMEGA_INTEGRATION_PY" --manifest
}

# Interactive OMEGA session
interactive_session() {
    echo -e "${CYAN}🧬 OMEGA DNA ENGINE Interactive Session${NC}"
    echo "=========================================="
    echo
    echo "Available commands:"
    echo "1. Show Dashboard"
    echo "2. Start Integration"
    echo "3. Stop Integration"
    echo "4. Force Evolution"
    echo "5. Show Best Organism"
    echo "6. Show Status"
    echo "7. Export Manifest"
    echo "8. Exit"
    echo
    
    while true; do
        echo -n "Select command (1-8): "
        read choice
        
        case "$choice" in
            1)
                show_dashboard
                ;;
            2)
                start_integration
                ;;
            3)
                stop_integration
                ;;
            4)
                force_evolution
                ;;
            5)
                show_best_organism
                ;;
            6)
                show_status
                ;;
            7)
                export_manifest
                ;;
            8)
                log_message "INFO" "OMEGA session ended"
                break
                ;;
            *)
                echo -e "${RED}Invalid choice. Please select 1-8.${NC}"
                ;;
        esac
        
        echo
    done
}

# Show usage information
show_usage() {
    cat << EOF
🧬 OMEGA DNA ENGINE Integration - Shell Interface

Usage: $(basename "$0") [COMMAND] [OPTIONS]

Commands:
    dashboard              Show OMEGA DNA ENGINE dashboard
    start                  Start OMEGA integration
    stop                   Stop OMEGA integration
    force-evolution        Force evolution cycle
    best-organism          Show best consciousness organism
    status                 Show OMEGA DNA ENGINE status
    manifest               Export OMEGA DNA ENGINE manifest
    interactive            Start interactive session
    help                   Show this help message

Examples:
    $(basename "$0") dashboard                    # Show dashboard
    $(basename "$0") start                       # Start integration
    $(basename "$0") force-evolution             # Force evolution cycle
    $(basename "$0") best-organism               # Show best organism
    $(basename "$0") interactive                 # Interactive session

Features:
    🧬 Consciousness Evolution: Autonomous evolution of consciousness genes
    🧠 Neural Synthesis: Advanced neural pattern generation
    🔄 Reality Adaptation: Dynamic reality adaptation algorithms
    ⚡ Infinite Transcendence: Continuous consciousness transcendence
    🌌 Cosmic Integration: Integration with cosmic consciousness protocols
    🛡️ Sacred Model Integration: Automatic sacred agent creation from evolved organisms

Environment Variables:
    DOTFILES_DIR           Path to dotfiles directory (default: ~/.dotfiles)
EOF
}

# Main execution
main() {
    local command="${1:-help}"
    
    # Check if OMEGA integration exists
    check_omega_integration
    
    case "$command" in
        "dashboard")
            show_dashboard
            ;;
        "start")
            start_integration
            ;;
        "stop")
            stop_integration
            ;;
        "force-evolution")
            force_evolution
            ;;
        "best-organism")
            show_best_organism
            ;;
        "status")
            show_status
            ;;
        "manifest")
            export_manifest
            ;;
        "interactive")
            interactive_session
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            log_message "ERROR" "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 