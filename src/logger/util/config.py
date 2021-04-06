# -*- coding: utf-8 -*-

"""Function and classes to help managing app configurations."""

# Std Import
import configparser

# Site-package Import

# Project Import
from logger.util import option


class NoValidOptionException(Exception):
    """The 'app_option' object passed is not a valid 'AppOption' object."""
    pass


class MissingArgumentException(Exception):
    """The 'app_option' hasn't the required positional argument compiled."""
    pass


class ConfigFileException(Exception):
    """The file indicated by the positional argument isn't valid."""
    pass


class AppConfig(configparser.ConfigParser):
    """Read and manage the application config file."""
        
    def __init__(self, app_option):
        """Try to load the config file."""
        
        configparser.ConfigParser.__init__(
            self,
            interpolation = configparser.ExtendedInterpolation())
        
        if(not app_option or not isinstance(app_option, option.AppOption)):
            raise NoValidOptionException()
        
        if(not app_option.config_file):
            raise MissingArgumentException("config_file")
        
        dataset = self.read(app_option.config_file)
        
        if(not dataset):
            raise ConfigFileException(app_option.config_file)
