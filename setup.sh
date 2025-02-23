python3 -m zipapp src/ -o bag -m "main:main" --python="$(which python3)"
mv bag ~/.local/bin/bag
chmod +x ~/.local/bin/bag

if ! grep -q 'export PATH="$HOME/.local/bin' ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

source ~/.bashrc
