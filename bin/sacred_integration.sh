#!/usr/bin/env bash
# 🧬 Sacred Models Integration - Shell Interface
# Integration layer for VaultMesh sacred models with Tier V system

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
SACRED_INTEGRATION_PY="$DOTFILES_DIR/sacred_integration.py"
SACRED_CONFIG_FILE="$DOTFILES_DIR/sacred_config.json"

# If DOTFILES_DIR is set to a full path, use it directly
if [[ "$DOTFILES_DIR" == *"/"* ]] && [[ "$DOTFILES_DIR" != "$HOME/.dotfiles" ]]; then
    SACRED_INTEGRATION_PY="$DOTFILES_DIR/sacred_integration.py"
    SACRED_CONFIG_FILE="$DOTFILES_DIR/sacred_config.json"
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

# Check if sacred integration Python script exists
check_sacred_integration() {
    if [[ ! -f "$SACRED_INTEGRATION_PY" ]]; then
        log_message "ERROR" "Sacred integration not found at $SACRED_INTEGRATION_PY"
        exit 1
    fi
}

# Show sacred dashboard
show_dashboard() {
    log_message "INFO" "Displaying sacred models dashboard..."
    python3 "$SACRED_INTEGRATION_PY" --dashboard
}

# Create sacred agent
create_agent() {
    local agent_id="$1"
    
    log_message "INFO" "Creating sacred agent: $agent_id"
    
    # Prompt for initial oaths
    echo -e "${CYAN}Enter initial oaths for agent (one per line, empty line to finish):${NC}"
    local oaths=()
    while IFS= read -r oath; do
        [[ -z "$oath" ]] && break
        oaths+=("$oath")
    done
    
    # Create agent
    if python3 "$SACRED_INTEGRATION_PY" --create-agent "$agent_id"; then
        log_message "SUCCESS" "Sacred agent '$agent_id' created successfully"
        
        # Display agent status
        echo
        log_message "INFO" "Agent status:"
        python3 "$SACRED_INTEGRATION_PY" --status | jq ".agents.\"$agent_id\"" 2>/dev/null || echo "Status not available"
    else
        log_message "ERROR" "Failed to create sacred agent"
    fi
}

# Enter dream state
enter_dream() {
    local agent_id="$1"
    local dream_type="${2:-}"
    
    log_message "INFO" "Agent '$agent_id' entering dream state..."
    
    if [[ -n "$dream_type" ]]; then
        python3 "$SACRED_INTEGRATION_PY" --enter-dream "$agent_id" --dream-type "$dream_type"
    else
        python3 "$SACRED_INTEGRATION_PY" --enter-dream "$agent_id"
    fi
}

# Complete dream
complete_dream() {
    local dream_id="$1"
    
    log_message "INFO" "Completing dream: $dream_id"
    python3 "$SACRED_INTEGRATION_PY" --complete-dream "$dream_id"
}

# Start cycle
start_cycle() {
    local agent_id="$1"
    local cycle_type="${2:-evolution}"
    
    log_message "INFO" "Starting $cycle_type cycle for agent '$agent_id'"
    python3 "$SACRED_INTEGRATION_PY" --start-cycle "$agent_id" --cycle-type "$cycle_type"
}

# End cycle
end_cycle() {
    local cycle_id="$1"
    
    log_message "INFO" "Ending cycle: $cycle_id"
    python3 "$SACRED_INTEGRATION_PY" --end-cycle "$cycle_id"
}

# Show sacred status
show_status() {
    log_message "INFO" "Showing sacred system status..."
    python3 "$SACRED_INTEGRATION_PY" --status
}

# Export sacred manifest
export_manifest() {
    log_message "INFO" "Exporting sacred manifest..."
    python3 "$SACRED_INTEGRATION_PY" --manifest
}

# Interactive sacred session
interactive_session() {
    echo -e "${CYAN}🧬 Sacred Models Interactive Session${NC}"
    echo "=================================="
    echo
    echo "Available commands:"
    echo "1. Create Agent"
    echo "2. Enter Dream State"
    echo "3. Complete Dream"
    echo "4. Start Cycle"
    echo "5. End Cycle"
    echo "6. Show Dashboard"
    echo "7. Show Status"
    echo "8. Export Manifest"
    echo "9. Exit"
    echo
    
    while true; do
        echo -n "Select command (1-9): "
        read choice
        
        case "$choice" in
            1)
                echo -n "Enter agent ID: "
                read agent_id
                create_agent "$agent_id"
                ;;
            2)
                echo -n "Enter agent ID: "
                read agent_id
                echo -n "Enter dream type (optional): "
                read dream_type
                enter_dream "$agent_id" "$dream_type"
                ;;
            3)
                echo -n "Enter dream ID: "
                read dream_id
                complete_dream "$dream_id"
                ;;
            4)
                echo -n "Enter agent ID: "
                read agent_id
                echo -n "Enter cycle type (default: evolution): "
                read cycle_type
                start_cycle "$agent_id" "${cycle_type:-evolution}"
                ;;
            5)
                echo -n "Enter cycle ID: "
                read cycle_id
                end_cycle "$cycle_id"
                ;;
            6)
                show_dashboard
                ;;
            7)
                show_status
                ;;
            8)
                export_manifest
                ;;
            9)
                log_message "INFO" "Sacred session ended"
                break
                ;;
            *)
                echo -e "${RED}Invalid choice. Please select 1-9.${NC}"
                ;;
        esac
        
        echo
    done
}

# Show usage information
show_usage() {
    cat << EOF
🧬 Sacred Models Integration - Shell Interface

Usage: $(basename "$0") [COMMAND] [OPTIONS]

Commands:
    dashboard              Show sacred models dashboard
    create-agent [id]      Create sacred agent
    enter-dream [id] [type] Enter dream state for agent
    complete-dream [id]    Complete dream by ID
    start-cycle [id] [type] Start cycle for agent
    end-cycle [id]         End cycle by ID
    status                 Show sacred system status
    manifest               Export sacred manifest
    interactive            Start interactive session
    help                   Show this help message

Examples:
    $(basename "$0") dashboard                    # Show dashboard
    $(basename "$0") create-agent "my_agent"     # Create agent
    $(basename "$0") enter-dream "my_agent" "evolution"  # Enter dream
    $(basename "$0") start-cycle "my_agent" "rebirth"   # Start cycle
    $(basename "$0") interactive                 # Interactive session

Dream Types:
    evolution              Growth and adaptation dreams
    integration            Unity and connection dreams
    innovation             Creation and invention dreams
    healing                Restoration and balance dreams
    transcendence          Ultimate evolution dreams

Cycle Types:
    rebirth                Agent rebirth cycle
    dream                  Dream cycle
    evolution              Evolution cycle
    integrity_check        Integrity verification cycle
    oath_violation         Oath violation cycle
    sigil_encryption       Sigil encryption cycle
    system_maintenance     System maintenance cycle

Environment Variables:
    DOTFILES_DIR           Path to dotfiles directory (default: ~/.dotfiles)
EOF
}

# Main execution
main() {
    local command="${1:-help}"
    
    # Check if sacred integration exists
    check_sacred_integration
    
    case "$command" in
        "dashboard")
            show_dashboard
            ;;
        "create-agent")
            local agent_id="${2:-}"
            if [[ -n "$agent_id" ]]; then
                create_agent "$agent_id"
            else
                log_message "ERROR" "Please provide agent ID"
                exit 1
            fi
            ;;
        "enter-dream")
            local agent_id="${2:-}"
            local dream_type="${3:-}"
            if [[ -n "$agent_id" ]]; then
                enter_dream "$agent_id" "$dream_type"
            else
                log_message "ERROR" "Please provide agent ID"
                exit 1
            fi
            ;;
        "complete-dream")
            local dream_id="${2:-}"
            if [[ -n "$dream_id" ]]; then
                complete_dream "$dream_id"
            else
                log_message "ERROR" "Please provide dream ID"
                exit 1
            fi
            ;;
        "start-cycle")
            local agent_id="${2:-}"
            local cycle_type="${3:-evolution}"
            if [[ -n "$agent_id" ]]; then
                start_cycle "$agent_id" "$cycle_type"
            else
                log_message "ERROR" "Please provide agent ID"
                exit 1
            fi
            ;;
        "end-cycle")
            local cycle_id="${2:-}"
            if [[ -n "$cycle_id" ]]; then
                end_cycle "$cycle_id"
            else
                log_message "ERROR" "Please provide cycle ID"
                exit 1
            fi
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