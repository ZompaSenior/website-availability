# -*- coding: utf-8 -*-

"""Description of the module."""

# Std Import
from datetime import datetime
import enum
import json
import re
import requests
import time

# Site-package Import
from kafka import KafkaProducer

# Project Import
from util import option
from util import config


class ReturnCode(enum.IntEnum):
    OK = 0
    OPTION_PARSER_ERROR = enum.auto()
    URL_LIST_FILE_NOT_VALID_ERROR = enum.auto()
    CONFIG_FILE_NOT_VALID_ERROR = enum.auto()
    CONSUMER_CREATION_ERROR = enum.auto()
    

ERROR_STATUS = -1
ERROR_DESCRIPTION_SERVER_UNREACHABLE = "Server unreachable"

ERROR_URL_LIST_FILE_NOT_VALID = "Url list file not valid"
ERROR_CONFIG_FILE_NOT_VALID = "Config file not valid"

def get_metric_info(url_config: dict):
    """Check website availability and retrieve information.
    
    Param:
        url (str): address of the website to check
        
    Return:
        (dict): information retrieved from the website check:
            - ts (datetime): exact moment of the check
            - url (str): url requested
            - response_time (float): time for the website responce
            - status (int): status code from the website
            - count_matches (int): number of matches of the regex
            - error (dict): an error description if something go wrong
    """
    
    # Initialize some variables
    ts = str(datetime.now())
    status = -1
    count_matches = -1
    response_time = -1.0
    
    try:
        # Memorize start time
        start = time.time()
        print(f"Requesting {url_config[config.KEY_URL]} ...")
        r = requests.get(url_config[config.KEY_URL])
        print(f"OK")
        # Register execution time
        response_time = time.time() - start
        status = r.status_code
        
        print("Searchin for RegEx ...")
        try:
            regex_to_search = url_config[config.KEY_REGEX]
            
            found_matches = re.findall(regex_to_search, r.text)
            
            if(found_matches):
                count_matches = len(found_matches)
                
            else:
                count_matches = 0
                
            print(f"Found {count_matches} matches")
        
        except KeyError:
            print("No RegEx provided")
        
        # No error to provide
        error = ""
        
    except Exception as e:
        response_time = time.time() - start
        error = "Server unreachable"
    
    return {
        "ts": ts,
        "url": url_config[config.KEY_URL],
        "response_time": response_time,
        "status": status,
        "count_matches": count_matches,
        "error": error
        }


def main(argv: list = None):
    """Main function for the application."""
    
    print("Creating application option parser ...")
    opt = option.AppOption()
    print("OK")
    
    print("Parsing option ...", end = '')
    if(opt.parse()):
        # problem will be provided from the parser ...
        return ReturnCode.OPTION_PARSER_ERROR
    
    print("OK")
    
    print("Reading url list ...")
    try:
        url_list = config.UrlList(opt)
    
    except Exception as e:
        print(ERROR_URL_LIST_FILE_NOT_VALID)
        return ReturnCode.URL_LIST_FILE_NOT_VALID_ERROR
    
    print("OK")

    print("Reading configuration ...")
    try:
        cfg = config.AppConfig(opt)
    
    except Exception as e:
        print(ERROR_CONFIG_FILE_NOT_VALID)
        return ReturnCode.CONFIG_FILE_NOT_VALID_ERROR
    
    print("OK")

    print("Creating Consumer ...")
    try:
        # Create the producer based on the config file parameters
        producer = KafkaProducer(
            bootstrap_servers = cfg['kafka']['server_address'],
            security_protocol = "SSL",
            ssl_cafile = cfg['kafka']['ssl_cafile'],
            ssl_certfile = cfg['kafka']['ssl_certfile'],
            ssl_keyfile = cfg['kafka']['ssl_keyfile'])
    
    except Exception as e:
        print(e)
        return ReturnCode.CONSUMER_CREATION_ERROR
        
    print("OK")
    
    while(True):
        try:
            # Test all the urls in the list
            for url_cfg in url_list.url_list:
                # Collect metris from url, and create an appropriate JSON string
                metric = json.dumps(get_metric_info(url_cfg), indent = 2)
                print(f"Complete metric: {metric}")
                print("Sending to Kafka...", end = '')
                producer.send(cfg['kafka']['topic_name'], metric.encode("utf-8"))
                print("OK")
                # Take a breath between url
                time.sleep(float(opt.pause))
            
            # Force sending of all messages
            producer.flush()
            
            # Take a breath between list scrolling
            time.sleep(float(opt.sleep_time))
        
        except KeyboardInterrupt:
            break
        
    return ReturnCode.OK

