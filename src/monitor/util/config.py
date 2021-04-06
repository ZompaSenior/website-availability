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
    """The 'app_option' hasn't the required positional argument compiled."""
    pass


class ConfigFileException(Exception):
    """The file indicated by the positional argument isn't valid."""
    pass


class UrlList():
    """"Basic class to manage option and loading of the URL list from file. """
    
    def __init__(self, app_option):
        """Load the url list from the file indicated in the command line options.
        
        Pars:
            option (AppOption): option object from command line"""
        
        # Initialize empty url list
        self.__url_list = []
        
        # Check to have a valid option object
        if(not app_option or not isinstance(app_option, option.AppOption)):
            raise NoValidOptionException()
        
        # Check to have the proper parameter compiled
        if(not app_option.url_list):
            raise MissingArgumentException(option.ARGUMENT_URL_LIST)
        
        # Try to read the file indicated by the option
        try:
            with open(str(app_option.url_list), "rt") as f:
                lines = f.readlines()
                self.__url_list = [url.strip() for url in lines]
        
        except:
            raise ConfigFileException()
    
    @property
    def url_list(self):
        """Read-only property for the url list."""
        
        return self.__url_list

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
