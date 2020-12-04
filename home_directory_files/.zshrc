# alias pip="pip3"
# alias python="python3"

# Starship (Demoing this for now - remove this and brew application in dotfiles if this is reverted)
eval "$(starship init zsh)"

# SYSCON RELATED ITEMS =============================================================================

# Node Version Manager
# This export is what is causing the Terminal to take an extra second to start up
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
