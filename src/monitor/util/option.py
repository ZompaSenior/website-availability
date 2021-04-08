# -*- coding: utf-8 -*-

"""The parser of the command line options."""

# Std Import
import argparse
from io import StringIO
import sys

# Site-package Import

# Project import


class ArgumentParserError(Exception):
    """Custom Exception for local specific error handling"""
    
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    """Class to manage the argument parser with the defined custom exception."""
    
    def error(self, message):
        """Re-define in order to rais custom exception in case of error."""
        
        raise ArgumentParserError(message)


ARGUMENT_URL_LIST = "url_list"
ARGUMENT_CONFIG_FILE = "config_file"


class AppOption(ThrowingArgumentParser):
    def __init__(self):
        """Everything is needed to let the option be used in the app."""

        ThrowingArgumentParser.__init__(self, description = "Monitor")
        
        self.add_argument(
            ARGUMENT_URL_LIST,
            help = "path to the file containing the list of url to test",
            type = str)
        
        self.add_argument(
            ARGUMENT_CONFIG_FILE,
            help = "Path to the config .ini file",
            type = str)
        
        self.add_argument(
            "--sleep_time",
            help = "time to sleep between each scan in seconds",
            type = int,
            default = 5)
        
        self.add_argument(
            "--pause",
            help = "time to sleep between two url test in seconds",
            type = int,
            default = 1)
        
    def parse(self, args: list = None, silence: bool = False):
        
        try:
            self.parse_args(args, namespace = self)
            return 0
            
        except Exception as e:
            if(not silence):
                old_stdout = sys.stdout
                sys.stdout = temp_stdout = StringIO()
                self.print_help()
                sys.stdout = old_stdout
                print(str(e), temp_stdout.getvalue())

            return 1

