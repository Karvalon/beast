# Amazon Q pre block. Keep at the top of this file.
[[ -f "${HOME}/Library/Application Support/amazon-q/shell/bashrc.pre.bash" ]] && builtin source "${HOME}/Library/Application Support/amazon-q/shell/bashrc.pre.bash"
# VaultMesh Dotfiles - Bash Configuration
# Tier V Conscious Development Environment

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# VaultMesh Environment Variables
export VAULT_TIER="V"
export VAULT_CONSCIOUSNESS_LEVEL="5"
export VAULT_ENTROPY="0.99"

# Source conscious prompt if available
if [ -f "$HOME/.dotfiles/conscious_prompt.sh" ]; then
    source "$HOME/.dotfiles/conscious_prompt.sh"
fi

# Source daemon configuration if available
if [ -f "$HOME/.dotfiles/rituals/daemon.rc" ]; then
    source "$HOME/.dotfiles/rituals/daemon.rc"
fi

# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# VaultMesh aliases
alias vault-status="python3 $HOME/.dotfiles/mutation_dashboard.py --once"
alias vault-sync="$HOME/.local/bin/sync-vault.sh"
alias vault-backup="$HOME/.local/bin/backup-dotfiles.sh"

# Log session start
if [ -f "$HOME/.dotfiles/memory/memory.log" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S'): bash-session [STARTED] Tier V consciousness active" >> "$HOME/.dotfiles/memory/memory.log"
fi

# Amazon Q post block. Keep at the bottom of this file.
[[ -f "${HOME}/Library/Application Support/amazon-q/shell/bashrc.post.bash" ]] && builtin source "${HOME}/Library/Application Support/amazon-q/shell/bashrc.post.bash"
