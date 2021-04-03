# -*- coding: utf-8 -*-

"""Description of the module."""

# Std Import
import unittest

# Site-package Import

# Project Import
from monitor.app import monitor
from monitor.util import option
from monitor.util import config
import os
import sys


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

class TestGetUrlList(unittest.TestCase):

    def test_no_option(self):
        with self.assertRaises(config.NoValidOptionException):
            config.get_url_list(None)
    
    def test_wrong_option(self):
        with self.assertRaises(config.NoValidOptionException):
            config.get_url_list(1)
    
    def test_option_with_no_url_list(self):
        o = option.AppOption()
        o.parse([], True)
        
        with self.assertRaises(config.MissingArgumentException):
            config.get_url_list(o)
    
    def test_option_with_wrong_url_list_file(self):
        o = option.AppOption()
        o.parse(["fake"], True)
        
        with self.assertRaises(config.ConfigFileException):
            config.get_url_list(o)
    
    def test_option_with_correct_url_list_file(self):
        o = option.AppOption()
        config_file = os.path.join(sys.path[0],
                              "monitor_url_list.txt")
        o.parse([config_file,], True)
        url_list = config.get_url_list(o)
        self.assertEqual(len(url_list), 3)
    


if __name__ == '__main__':
    unittest.main()
    
    
    