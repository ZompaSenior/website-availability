# -*- coding: utf-8 -*-

"""Monitor Unit Tests."""

# Std Import
import os
import sys
import unittest

# Site-package Import

# Project Import
from monitor.app import monitor
from monitor.util import option
from monitor.util import config


class TestGetMetricInfo(unittest.TestCase):

    def test_correct_url(self):
        url = "http://www.google.com"
        info = monitor.get_metric_info(url)
        self.assertEqual(info["url"], url)
        self.assertEqual(info["status"], 200)
        self.assertEqual(
            info["body"][:50],
            "<!doctype html><html itemscope=\"\" itemtype=\"http:/")
        self.assertEqual(info["error"], "")

    def test_wrong_url(self):
        url = "https://www.python.org/pippo"
        info = monitor.get_metric_info(url)
        self.assertEqual(info["url"], url)
        self.assertEqual(info["status"], 404)
        self.assertEqual(
            info["body"][:50],
            "<!doctype html>\n<!--[if lt IE 7]>   <html class=\"n")
        self.assertEqual(info["error"], "")

    def test_wrong_server(self):
        url = "https://www.xyzhhhggffdd.com"
        info = monitor.get_metric_info(url)
        self.assertEqual(info["url"], url)
        self.assertEqual(info["status"], monitor.ERROR_STATUS)
        self.assertEqual(info["body"], "")
        self.assertEqual(
            info["error"],
            monitor.ERROR_DESCRIPTION_SERVER_UNREACHABLE)


class TestOptions(unittest.TestCase):
    
    def test_no_option(self):
        app_option = option.AppOption()
        self.assertEqual(app_option.parse([], True), 1)
        
    def test_config_file_option(self):
        app_option = option.AppOption()
        self.assertEqual(app_option.parse([
            'fake_url_list_file',
            'fake_config_file'], True), 0)


class TestGetUrlList(unittest.TestCase):

    def test_no_option(self):
        with self.assertRaises(config.NoValidOptionException):
            config.UrlList(None)
    
    def test_wrong_option(self):
        with self.assertRaises(config.NoValidOptionException):
            config.UrlList(1)
    
    def test_option_with_no_url_list(self):
        o = option.AppOption()
        o.parse([], True)
        
        with self.assertRaises(config.MissingArgumentException):
            config.UrlList(o)
    
    def test_option_with_wrong_url_list_file(self):
        o = option.AppOption()
        o.parse(['fake_url_list_file',
            'fake_config_file'], True)
        
        with self.assertRaises(config.ConfigFileException):
            config.UrlList(o)
    
    def test_option_with_correct_url_list_file(self):
        o = option.AppOption()
        config_file = os.path.join(sys.path[0],
                              "monitor_url_list.txt")
        o.parse([config_file,], True)
        url_list = config.UrlList(o)
        self.assertEqual(len(url_list.url_list), 3)
    

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
        o.parse(['fake_url_list_file',
                 'fake_config_file'])
        
        with self.assertRaises(config.ConfigFileException):
            config.AppConfig(o)
    
    def test_option_with_correct_config_file(self):
        o = option.AppOption()
        config_file = os.path.join(sys.path[0],
                              "monitor.ini")
        o.parse(['fake_url_list_file',
                 config_file,], True)
        app_config = config.AppConfig(o)
        
        self.assertEqual(app_config["kafka"]["server_address"], "aaa")


if __name__ == '__main__':
    unittest.main()
    
    
    