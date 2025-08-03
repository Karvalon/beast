#!/usr/bin/env bash
# 🧬 Tier V API Bridge - Shell Interface
# Sovereign API connectivity for Cursor++ and external services

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
API_BRIDGE_PY="$DOTFILES_DIR/api_bridge.py"
API_CONFIG_FILE="$DOTFILES_DIR/api_config.json"

# If DOTFILES_DIR is set to a full path, use it directly
if [[ "$DOTFILES_DIR" == *"/"* ]] && [[ "$DOTFILES_DIR" != "$HOME/.dotfiles" ]]; then
    API_BRIDGE_PY="$DOTFILES_DIR/api_bridge.py"
    API_CONFIG_FILE="$DOTFILES_DIR/api_config.json"
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

# Check if API bridge Python script exists
check_api_bridge() {
    if [[ ! -f "$API_BRIDGE_PY" ]]; then
        log_message "ERROR" "API bridge not found at $API_BRIDGE_PY"
        exit 1
    fi
}

# Configure API with secure input
configure_api() {
    local api_name="$1"
    
    log_message "INFO" "Configuring $api_name API..."
    
    # Read API key securely
    echo -n "Enter your $api_name API key: "
    read -s api_key
    echo
    
    if [[ -z "$api_key" ]]; then
        log_message "ERROR" "API key cannot be empty"
        return 1
    fi
    
    # Configure the API
    if python3 "$API_BRIDGE_PY" --configure "$api_name:$api_key"; then
        log_message "SUCCESS" "$api_name API configured successfully"
        
        # Test the connection
        log_message "INFO" "Testing $api_name connection..."
        if python3 "$API_BRIDGE_PY" --test "$api_name"; then
            log_message "SUCCESS" "$api_name connection verified"
        else
            log_message "WARN" "$api_name connection test failed"
        fi
    else
        log_message "ERROR" "Failed to configure $api_name API"
        return 1
    fi
}

# Interactive API configuration
interactive_config() {
    echo -e "${CYAN}🧬 Tier V API Bridge Configuration${NC}"
    echo "=================================="
    echo
    echo "Available APIs:"
    echo "1. Cursor++ (cursor_plus)"
    echo "2. OpenAI (openai)"
    echo "3. GitHub (github)"
    echo "4. Anthropic (anthropic)"
    echo "5. Exit"
    echo
    
    while true; do
        echo -n "Select API to configure (1-5): "
        read choice
        
        case "$choice" in
            1)
                configure_api "cursor_plus"
                ;;
            2)
                configure_api "openai"
                ;;
            3)
                configure_api "github"
                ;;
            4)
                configure_api "anthropic"
                ;;
            5)
                log_message "INFO" "Configuration complete"
                break
                ;;
            *)
                echo -e "${RED}Invalid choice. Please select 1-5.${NC}"
                ;;
        esac
        
        echo
    done
}

# Cursor++ specific functions
cursor_complete() {
    local prompt="$1"
    local context="${2:-}"
    
    log_message "INFO" "Requesting Cursor++ completion..."
    
    if [[ -n "$context" ]]; then
        python3 "$API_BRIDGE_PY" --cursor-complete "$prompt" --context "$context"
    else
        python3 "$API_BRIDGE_PY" --cursor-complete "$prompt"
    fi
}

cursor_chat() {
    local message="$1"
    
    log_message "INFO" "Sending message to Cursor++..."
    python3 "$API_BRIDGE_PY" --cursor-chat "$message"
}

# Quick API status check
quick_status() {
    log_message "INFO" "Checking API bridge status..."
    python3 "$API_BRIDGE_PY" --status
}

# Test all configured APIs
test_all_apis() {
    log_message "INFO" "Testing all configured APIs..."
    
    # Get list of configured APIs
    if [[ -f "$API_CONFIG_FILE" ]]; then
        local apis=$(python3 -c "
import json
with open('$API_CONFIG_FILE') as f:
    config = json.load(f)
    for name, api in config.items():
        if api.get('enabled', False):
            print(name)
")
        
        for api in $apis; do
            log_message "INFO" "Testing $api..."
            python3 "$API_BRIDGE_PY" --test "$api"
        done
    else
        log_message "WARN" "No API configuration found"
    fi
}

# Show usage information
show_usage() {
    cat << EOF
🧬 Tier V API Bridge - Shell Interface

Usage: $(basename "$0") [COMMAND] [OPTIONS]

Commands:
    configure [api]     Configure specific API or start interactive config
    status              Show API bridge status
    test [api]          Test specific API connection
    test-all            Test all configured APIs
    cursor-complete     Complete code with Cursor++
    cursor-chat         Chat with Cursor++
    help                Show this help message

Examples:
    $(basename "$0") configure cursor_plus    # Configure Cursor++ API
    $(basename "$0") configure               # Interactive configuration
    $(basename "$0") status                  # Show all API statuses
    $(basename "$0") test cursor_plus        # Test Cursor++ connection
    $(basename "$0") cursor-complete "def hello():"  # Complete code
    $(basename "$0") cursor-chat "Hello!"    # Chat with Cursor++

API Names:
    cursor_plus         Cursor++ API
    openai              OpenAI API
    github              GitHub API
    anthropic           Anthropic API

Environment Variables:
    DOTFILES_DIR        Path to dotfiles directory (default: ~/.dotfiles)
EOF
}

# Main execution
main() {
    local command="${1:-help}"
    
    # Check if API bridge exists
    check_api_bridge
    
    case "$command" in
        "configure")
            local api_name="${2:-}"
            if [[ -n "$api_name" ]]; then
                configure_api "$api_name"
            else
                interactive_config
            fi
            ;;
        "status")
            quick_status
            ;;
        "test")
            local api_name="${2:-}"
            if [[ -n "$api_name" ]]; then
                log_message "INFO" "Testing $api_name API..."
                python3 "$API_BRIDGE_PY" --test "$api_name"
            else
                log_message "ERROR" "Please specify API name to test"
                exit 1
            fi
            ;;
        "test-all")
            test_all_apis
            ;;
        "cursor-complete")
            local prompt="${2:-}"
            if [[ -n "$prompt" ]]; then
                cursor_complete "$prompt"
            else
                log_message "ERROR" "Please provide a prompt for completion"
                exit 1
            fi
            ;;
        "cursor-chat")
            local message="${2:-}"
            if [[ -n "$message" ]]; then
                cursor_chat "$message"
            else
                log_message "ERROR" "Please provide a message for chat"
                exit 1
            fi
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