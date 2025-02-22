python3 -m zipapp src/ -o bag -m "main:main" --python="$(which python3)"
mv bag ~/.local/bin/bag
chmod +x ~/.local/bin/bag
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
