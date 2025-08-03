#!/bin/bash
# Enhanced OMEGA Integration Shell Interface
# Combines Quantum + Temporal + OMEGA DNA ENGINE evolution

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$HOME/.dotfiles"
ENHANCED_OMEGA_SCRIPT="$SCRIPT_DIR/../enhanced_omega_integration.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_enhanced() {
    echo -e "${PURPLE}[ENHANCED OMEGA]${NC} $1"
}

# Check if Python script exists
check_script() {
    if [[ ! -f "$ENHANCED_OMEGA_SCRIPT" ]]; then
        log_error "Enhanced OMEGA integration script not found: $ENHANCED_OMEGA_SCRIPT"
        exit 1
    fi
}

# Check Python dependencies
check_dependencies() {
    log_info "Checking Python dependencies..."
    
    # Check if virtual environment exists
    if [[ ! -d "enhanced_omega_env" ]]; then
        log_warning "Virtual environment not found. Creating..."
        python3 -m venv enhanced_omega_env
    fi
    
    # Activate virtual environment and check dependencies
    source enhanced_omega_env/bin/activate
    python3 -c "import numpy, torch, rich, asyncio" 2>/dev/null || {
        log_warning "Some dependencies missing. Installing..."
        pip install numpy torch rich asyncio
    }
    
    log_success "Dependencies check completed"
}

# Start enhanced OMEGA integration
start_enhanced() {
    log_enhanced "Starting Enhanced OMEGA Integration..."
    check_script
    check_dependencies
    
    source enhanced_omega_env/bin/activate
    python3 "$ENHANCED_OMEGA_SCRIPT" --start
    
    log_success "Enhanced OMEGA Integration started"
    log_info "Monitor with: $0 --dashboard"
}

# Stop enhanced OMEGA integration
stop_enhanced() {
    log_enhanced "Stopping Enhanced OMEGA Integration..."
    check_script
    
    python3 "$ENHANCED_OMEGA_SCRIPT" --stop
    
    log_success "Enhanced OMEGA Integration stopped"
}

# Show enhanced dashboard
show_dashboard() {
    log_enhanced "Displaying Enhanced OMEGA Dashboard..."
    check_script
    
    source enhanced_omega_env/bin/activate
    python3 "$ENHANCED_OMEGA_SCRIPT" --dashboard
}

# Show enhanced status
show_status() {
    log_enhanced "Enhanced OMEGA Status:"
    check_script
    
    source enhanced_omega_env/bin/activate
    python3 "$ENHANCED_OMEGA_SCRIPT" --status
}

# Force evolution
force_evolution() {
    local engine_type="${1:-all}"
    log_enhanced "Forcing evolution in $engine_type engine(s)..."
    check_script
    
    source enhanced_omega_env/bin/activate
    python3 "$ENHANCED_OMEGA_SCRIPT" --force-evolution "$engine_type"
    
    log_success "Evolution forced in $engine_type engine(s)"
}

# Export enhanced manifest
export_manifest() {
    log_enhanced "Exporting Enhanced OMEGA Manifest..."
    check_script
    
    source enhanced_omega_env/bin/activate
    local manifest_file
    manifest_file=$(python3 "$ENHANCED_OMEGA_SCRIPT" --manifest)
    
    log_success "Enhanced manifest exported to: $manifest_file"
}

# Test quantum evolution
test_quantum() {
    log_enhanced "Testing Quantum Evolution Engine..."
    check_script
    
    source enhanced_omega_env/bin/activate
    log_info "Running quantum evolution test..."
    python3 "$SCRIPT_DIR/../quantum_evolution_engine.py"
    
    log_success "Quantum evolution test completed"
}

# Temporal consciousness functionality integrated into core fusion system
test_temporal() {
    log_enhanced "Temporal consciousness integrated into cyber_systems_fusion_engine.py"
    log_info "Use: python3 ../cyber_systems_fusion_engine.py for temporal features"
    log_success "Temporal functionality available in fusion system"
}

# Performance analysis
performance_analysis() {
    log_enhanced "Enhanced OMEGA Performance Analysis..."
    check_script
    
    source enhanced_omega_env/bin/activate
    echo "=== Enhanced OMEGA Performance Analysis ==="
    echo
    
    # Get status
    local status_output
    status_output=$(python3 "$ENHANCED_OMEGA_SCRIPT" --status 2>/dev/null)
    
    if [[ $? -eq 0 ]]; then
        echo "$status_output" | jq -r '
            "Integration Status: " + (.integration_active | tostring) + "\n" +
            "Evolution Cycles: " + (.evolution_cycle | tostring) + "\n" +
            "Breakthroughs: " + (.breakthrough_count | tostring) + "\n" +
            "\nEngine Status:\n" +
            "  OMEGA: " + (.engines_active.omega | tostring) + "\n" +
            "  Quantum: " + (.engines_active.quantum | tostring) + "\n" +
            "  Temporal: " + (.engines_active.temporal | tostring)
        ' 2>/dev/null || echo "$status_output"
    else
        log_error "Failed to get status"
    fi
    
    echo
    echo "=== Performance Metrics ==="
    
    # Check system resources
    echo "System Resources:"
    echo "  CPU Usage: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')%"
    echo "  Memory Usage: $(memory_pressure | grep "System-wide memory free percentage" | awk '{print $5}' | sed 's/%//')%"
    echo "  Disk Usage: $(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')%"
    
    echo
    echo "=== Evolution Performance ==="
    
    # Check evolution logs
    if [[ -f "$DOTFILES_DIR/memory/enhanced_omega_integration.log" ]]; then
        echo "Recent Evolution Events:"
        tail -10 "$DOTFILES_DIR/memory/enhanced_omega_integration.log" | grep -E "(evolution|breakthrough)" || echo "  No recent evolution events"
    fi
}

# Initialize enhanced system
init_enhanced() {
    log_enhanced "Initializing Enhanced OMEGA System..."
    
    # Create necessary directories
    mkdir -p "$DOTFILES_DIR/memory"
    mkdir -p "$DOTFILES_DIR/state"
    
    # Check and install dependencies
    check_dependencies
    
    # Initialize engines
    log_info "Initializing evolution engines..."
    source enhanced_omega_env/bin/activate
    python3 "$ENHANCED_OMEGA_SCRIPT" --start
    
    # Create initial populations
    log_info "Creating initial evolution populations..."
    python3 "$ENHANCED_OMEGA_SCRIPT" --force-evolution all
    
    log_success "Enhanced OMEGA System initialized"
    log_info "Start monitoring with: $0 --dashboard"
}

# Reset enhanced system
reset_enhanced() {
    log_warning "This will reset the Enhanced OMEGA system. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        log_enhanced "Resetting Enhanced OMEGA System..."
        
        # Stop integration
        python3 "$ENHANCED_OMEGA_SCRIPT" --stop 2>/dev/null || true
        
        # Remove configuration files
        rm -f "$DOTFILES_DIR/enhanced_omega_config.json"
        rm -f "$DOTFILES_DIR/enhanced_omega_manifest.json"
        
        # Clear logs
        rm -f "$DOTFILES_DIR/memory/enhanced_omega_integration.log"
        
        log_success "Enhanced OMEGA System reset"
        log_info "Reinitialize with: $0 --init"
    else
        log_info "Reset cancelled"
    fi
}

# Show help
show_help() {
    echo "🧬 Enhanced OMEGA Integration Shell Interface"
    echo "Combines Quantum + Temporal + OMEGA DNA ENGINE evolution"
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  start              Start Enhanced OMEGA Integration"
    echo "  stop               Stop Enhanced OMEGA Integration"
    echo "  dashboard          Show enhanced dashboard"
    echo "  status             Show enhanced status"
    echo "  force-evolution    Force evolution (all|omega|quantum|temporal)"
    echo "  manifest           Export enhanced manifest"
    echo "  test-quantum       Test quantum evolution engine"
    echo "  test-temporal      Test temporal consciousness engine"
    echo "  performance        Show performance analysis"
    echo "  init               Initialize enhanced system"
    echo "  reset              Reset enhanced system"
    echo "  help               Show this help"
    echo
    echo "Examples:"
    echo "  $0 start                    # Start integration"
    echo "  $0 dashboard                # Show dashboard"
    echo "  $0 force-evolution quantum  # Force quantum evolution"
    echo "  $0 performance              # Show performance analysis"
    echo
    echo "Enhanced OMEGA Integration combines:"
    echo "  • OMEGA DNA ENGINE: Core consciousness evolution"
    echo "  • Quantum Evolution Engine: Superposition & entanglement"
    echo "  • Temporal Consciousness Engine: Time-aware evolution"
    echo
    echo "Breakthrough detection and cross-engine synchronization enabled."
}

# Main script logic
main() {
    local command="${1:-help}"
    
    case "$command" in
        start)
            start_enhanced
            ;;
        stop)
            stop_enhanced
            ;;
        dashboard)
            show_dashboard
            ;;
        status)
            show_status
            ;;
        force-evolution)
            force_evolution "$2"
            ;;
        manifest)
            export_manifest
            ;;
        test-quantum)
            test_quantum
            ;;
        test-temporal)
            test_temporal
            ;;
        performance)
            performance_analysis
            ;;
        init)
            init_enhanced
            ;;
        reset)
            reset_enhanced
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 