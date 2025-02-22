echo '#!/usr/bin/env python3' | cat - main.py > ~/.local/bin/bag
chmod +x ~/.local/bin/bag
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
