# -*- coding: utf-8 -*-

"""Function and classes to help managing app configurations."""

# Std Import
import configparser

# Site-package Import

# Project Import
from monitor.util import option


class NoValidOptionException(Exception):
    """The 'app_option' object passed is not a valid 'AppOption' object."""
    pass


class MissingArgumentException(Exception):
    """The 'app_option' hasn't the 'url_list' positional argument compiled."""
    pass


class ConfigFileException(Exception):
    """The file indicated by the 'url_list' positional argument isn't valid."""
    pass


def get_url_list(app_option):
    """Load the url list from the file indicated in the command line options.
    
    Pars:
        option ()"""
    
    if(not app_option or not isinstance(app_option, option.AppOption)):
        raise NoValidOptionException()
    
    if(not app_option.url_list):
        raise MissingArgumentException("url_list")
    
    try:
        with open(str(app_option.url_list), "rt") as f:
            lines = f.readlines()
            return [url for url in lines]
    
    except:
        raise ConfigFileException()
    

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
        
        try:
            self.read(app_option.config_file)
            
        except:
            raise ConfigFileException(app_option.config_file)
