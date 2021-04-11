# -*- coding: utf-8 -*-

"""Logger is an utility that store metrics about websites from a Kafka server."""

__license__ = "GPL 3"
__version__ = "0.0.1"
__author__ = "Luca Zomparelli"

# Standard Import
import os
import sys

# Site-package Import

# Project Import
from app import logger

if __name__ == "__main__":
    # Preparatory settings
    os.environ.setdefault("PARSERPATH", sys.path[0])

    sys.exit(logger.main(sys.argv))
