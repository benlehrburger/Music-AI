# Author: Ben Lehrburger
# Project: Music & AI
# Script: Easy install/uninstall from within script

import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def uninstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])
