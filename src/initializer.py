from typing import Tuple, List

import os
import re
import shutil
import subprocess
from getpass import getpass, getuser
from utils.printutil import log_message

REQUIRE_SUDO_MESSAGE = "You need sudo preivilage to grant permissing to install, would you like to proceed (y/n|Y/N|yes/no|YES/NO): "
AG_DOESNT_EXIST_ERROR = f"ag command doesnt exist, you need to install it."
UNKNOWN_DISTRO_ERROR = "Failed to detect linux distribution"
INSTALLER_NOT_FOUND_ERROR = "Failed to identify installer"

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


def identify_distro() -> Tuple[str, str]:
    ### Not sure if lsb-release is avilable only on debian based distros
    os_release_file = "/etc/os-release"
    lsb_release_file = "/etc/lsb-release"

    distro_name = None

    if os.path.exists(os_release_file):
        with open(os_release_file, "r") as file:
            match = re.search(r'^ID="?(\w+)"?$', file.read(), re.MULTILINE)
    elif os.path.exists(lsb_release_file):
        with open(lsb_release_file, "r") as file:
            match = re.search(r'DISTRIB_ID="?(\w+)"?$', file.read(), re.MULTILINE)
    else:
        raise Exception(log_message(UNKNOWN_DISTRO_ERROR, "error", True))

    if not match:
        raise Exception(log_message(UNKNOWN_DISTRO_ERROR, "error", True))

    distro_name = match.group(1).lower()

    install_command = PACKAGE_INSTALLER_COMMANDS.get(distro_name)
    if not install_command:
        raise Exception(log_message(INSTALLER_NOT_FOUND_ERROR, "error", True))

    return distro_name, install_command


def grant_sudo_previlage(install_command: List[str] | Tuple[str]):
    retry_count = 0

    while True:
        password = getpass(f"password for {getuser()}: ")

        try:
            process = subprocess.Popen(
                ["sudo", "-S", *install_command],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            _, stderr = process.communicate(input=password)
            password = ""

            if process.returncode == 0:
                log_message("Successfully installed", log_type="success")
                break
            else:
                retry_count += 1
                errmsg = "Incorrect password" if "incorrect" in stderr else stderr0
                log_message(errmsg, log_type="error")
                if retry_count == 3:
                    log_message("Max retries reached, exit...")
                    break
            process.kill()
        except Exception as e:
            print(e)
            process.kill()
            break


def check_dep_exists():
    return shutil.which("ag") is not None


def prompt_install_request():
    message = log_message(REQUIRE_SUDO_MESSAGE, "warning", True)

    while True:
        choice = input(message).lower()
        if choice not in ("y", "n", "yes", "no"):
            log_message("Enter valid option", log_type="warning")
            continue
        elif choice == "n":
            log_message("Operation cancelled")
            return None
        elif choice == "y":
            return True


def init():
    distro, install_command = identify_distro()
    if not check_dep_exists():
        if prompt_install_request():
            grant_sudo_previlage(install_command)
