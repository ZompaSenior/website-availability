# -*- coding: utf-8 -*-

"""Monitor is an utility that scan for website from a list and send metric to
a Kafka server."""

__license__ = "GPL 3"
__version__ = "0.0.1"
__author__ = "Luca Zomparelli"

# Standard Import
import os
import sys

# Site-package Import

# Project Import
from app import monitor

if __name__ == "__main__":
    # Preparatory settings
    os.environ.setdefault("PYTHONPATH", sys.path[0])

    sys.exit(monitor.main(sys.argv))
