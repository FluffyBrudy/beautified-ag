PACKAGE_INSTALLER_COMMANDS = {
    "ubuntu": ["apt", "install", "silversearcher-ag"],
    "debian": ["apt", "install", "silversearcher-ag"],
    "linuxmint": ["apt", "install", "silversearcher-ag"],
    "fedora": ["dnf", "install", "the_silver_searcher"],
    ### not checking version may require dnf for v8 in centos
    "centos": ["yum", "install", "the_silver_searcher"],
    "rhel": ["yum", "install", "the_silver_searcher"],
    "arch": ["pacman", "-S", "the_silver_searcher"],
    "manjaro": ["pacman", "-S", "the_silver_searcher"],
    "opensuse": ["zypper", "install", "the_silver_searcher"],
    "gentoo": ["emerge", "app-text/the_silver_searcher"],
    "kali": ["apt", "install", "silversearcher-ag"],
    "elementary": ["apt", "install", "silversearcher-ag"],
    "slackware": ["slackpkg", "install", "the_silver_searcher"],
    "void": ["xbps-install", "-S", "the_silver_searcher"],
}

TERMINAL_MAP = {
    "ubuntu": "gnome-terminal",
    "debian": "gnome-terminal",
    "linuxmint": "gnome-terminal",
    "fedora": "gnome-terminal",
    "centos": "gnome-terminal",
    "rhel": "gnome-terminal",
    "arch": "konsole",
    "manjaro": "konsole",
    "opensuse": "konsole",
    "gentoo": "xterm",
    "kali": "gnome-terminal",
    "elementary": "pantheon-terminal",
    "slackware": "xterm",
    "void": "xterm",
}
