# -*- coding: utf-8 -*-

"""Logger Unit Tests."""

# Std Import
import os
import sys
import unittest

# Site-package Import


# Project Import
from logger.util import config
from logger.util import db
from logger.util import option


class TestOption(unittest.TestCase):
    
    def test_no_option(self):
        app_option = option.AppOption()
        self.assertEqual(app_option.parse(silence = True), 1)
        
    def test_config_file_option(self):
        app_option = option.AppOption()
        self.assertEqual(app_option.parse(['fake'], True), 0)


class TestConfig(unittest.TestCase):

    def test_no_option(self):
        with self.assertRaises(config.NoValidOptionException):
            config.AppConfig(None)
    
    def test_wrong_option(self):
        with self.assertRaises(config.NoValidOptionException):
            config.AppConfig(1)
    
    def test_option_with_no_config_file(self):
        o = option.AppOption()
        o.parse([], True)
        
        with self.assertRaises(config.MissingArgumentException):
            config.AppConfig(o)
    
    def test_option_with_wrong_config_file(self):
        o = option.AppOption()
        o.parse(["/fake"])
        
        with self.assertRaises(config.ConfigFileException):
            app_config = config.AppConfig(o)
    
    def test_option_with_correct_config_file(self):
        o = option.AppOption()
        config_file = os.path.join(sys.path[0],
                              "logger.ini")
        o.parse([config_file,], True)
        app_config = config.AppConfig(o)
        
        self.assertEqual(app_config["kafka"]["server_address"], "aaa")
        self.assertEqual(app_config["postgresql"]["host"], "hhh")


class TestDatabaseCreation(unittest.TestCase):
    
    def get_config_file(self):
        o = option.AppOption()
        config_file = "/home/luca/Dropbox/Z-Work/Aiven/Logger/logger.ini"
        o.parse([config_file,], True)
        app_config = config.AppConfig(o)
        
        return app_config

    def x_test_table_absence(self):
        app_config = self.get_config_file()
        app_db = db.AppDB(app_config)
        

if __name__ == '__main__':
    unittest.main()
