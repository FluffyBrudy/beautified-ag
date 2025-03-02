#!/bin/bash
mkdir -p ~/.local/share/bash-completion/completions/

cat << 'EOF' > ~/.local/share/bash-completion/completions/bag

_bag_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    
    opts="--dir -h --help"

    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    if [[ "${prev}" == "--dir" ]]; then
        COMPREPLY=( $(compgen -d -- "${cur}") )
        return 0
    fi

    return 0
}


complete -F _bag_completion bag
EOF


chmod +x ~/.local/share/bash-completion/completions/bag


python3 -m zipapp src/ -o bag -m "main:main" --python="$(which python3)"


mv bag ~/.local/bin/bag
chmod +x ~/.local/bin/bag


if ! grep -q 'export PATH="$HOME/.local/bin' ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi


source ~/.bashrc
source ~/.local/share/bash-completion/completions/bag

echo "Setup complete."
