# -*- coding: utf-8 -*-

"""Monitor Unit Tests."""

# Std Import
import os
import sys
import unittest

# Site-package Import

# Project Import
# aAdding the project source path as first
current_path = sys.path[0]
new_path = os.path.normpath(
    os.path.join(sys.path[0], "..", "..", "src", "monitor"))
sys.path.insert(0, new_path)

from app import monitor
from util import option
from util import config


class TestGetMetricInfo(unittest.TestCase):

    def test_correct_url_correct_regex(self):
        url_cfg = {
            config.KEY_URL: "https://www.python.org/",
            config.KEY_REGEX: '<meta name="application-name" content="Python.org">'}
        
        info = monitor.get_metric_info(url_cfg)
        self.assertEqual(info["url"], url_cfg[config.KEY_URL])
        self.assertEqual(info["status"], 200)
        self.assertEqual(info["count_matches"], 1)
        self.assertEqual(info["error"], "")

    def test_correct_url_wrong_regex(self):
        url_cfg = {
            config.KEY_URL: "https://www.python.org/",
            config.KEY_REGEX: '<meta name="appplication-name" content="Python.org">'}

        info = monitor.get_metric_info(url_cfg)
        self.assertEqual(info["url"], url_cfg[config.KEY_URL])
        self.assertEqual(info["status"], 200)
        self.assertEqual(info["count_matches"], 0)
        self.assertEqual(info["error"], "")

    def test_wrong_url_correct_regex(self):
        url_cfg = {
            config.KEY_URL: "https://www.python.org/pippo",
            config.KEY_REGEX: 'Error 404: File not Found'}

        info = monitor.get_metric_info(url_cfg)
        self.assertEqual(info["url"], url_cfg[config.KEY_URL])
        self.assertEqual(info["status"], 404)
        self.assertEqual(info["count_matches"], 1)
        self.assertEqual(info["error"], "")

    def test_wrong_url_wrong_regex(self):
        url_cfg = {
            config.KEY_URL: "https://www.python.org/pippo",
            config.KEY_REGEX: 'Error 555: File not Found'}

        info = monitor.get_metric_info(url_cfg)
        self.assertEqual(info["url"], url_cfg[config.KEY_URL])
        self.assertEqual(info["status"], 404)
        self.assertEqual(info["count_matches"], 0)
        self.assertEqual(info["error"], "")

    def test_wrong_server(self):
        url_cfg = {
            config.KEY_URL: "https://www.xyzhhhggffdd.com",
            config.KEY_REGEX: ''}

        info = monitor.get_metric_info(url_cfg)
        self.assertEqual(info["url"], url_cfg[config.KEY_URL])
        self.assertEqual(info["status"], monitor.ERROR_STATUS)
        self.assertEqual(info["count_matches"], -1)
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
        config_file = os.path.join(current_path,
                              "monitor_url_list.txt")
        o.parse([config_file,], True)
        url_list = config.UrlList(o)
        self.assertEqual(len(url_list.url_list), 5)
    

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
        config_file = os.path.join(current_path,
                              "monitor.ini")
        o.parse(['fake_url_list_file',
                 config_file,], True)
        app_config = config.AppConfig(o)
        
        self.assertEqual(app_config["kafka"]["server_address"], "aaa")


if __name__ == '__main__':
    unittest.main()
    
    
    