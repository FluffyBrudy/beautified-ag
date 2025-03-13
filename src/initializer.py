from typing import Tuple, List

import os
import re
import shlex
import shutil
import subprocess
from getpass import getpass, getuser
from utils.printutil import log_message
from constants.installer import *
from constants.errors import *

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

    return distro_name


def grant_sudo_previlage(distro: str):
    retry_count = 0

    install_command = PACKAGE_INSTALLER_COMMANDS.get(distro)
    if not install_command:
        log_message(INSTALLER_NOT_FOUND_ERROR, "error")
        exit(1)

    while True:
        try:
            process = subprocess.Popen(
                ["sudo", "-S", *install_command],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            _, stderr = process.communicate(input=getpass(f"password for {getuser()}: "))

            if process.returncode == 0:
                log_message("Successfully installed", log_type="success")
                break
            else:
                retry_count += 1
                errmsg = "Incorrect password" if "incorrect" in stderr else stderr
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
    log_message("Note that if you have sudo command already run then even if you pass wrong password installation will proceed", "warning")
    distro = identify_distro()
    if not check_dep_exists():
        if prompt_install_request():
            grant_sudo_previlage(distro)

if __name__ == "__main__":
    init()