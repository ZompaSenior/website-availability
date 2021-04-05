# -*- coding: utf-8 -*-

"""Description of the module."""

# Std Import
from datetime import datetime
import json
import requests
import time
import enum

# Site-package Import
from kafka import KafkaProducer

# Project Import
from monitor.util import option
from monitor.util import config


class ReturnCode(enum.IntEnum):
    OK = 0
    OPTION_PARSER_ERROR = enum.auto()
    URL_LIST_FILE_NOT_VALID_ERROR = enum.auto()
    CONFIG_FILE_NOT_VALID_ERROR = enum.auto()
    

ERROR_STATUS = -1
ERROR_DESCRIPTION_SERVER_UNREACHABLE = "Server unreachable"

ERROR_URL_LIST_FILE_NOT_VALID = "Url list file not valid"
ERROR_CONFIG_FILE_NOT_VALID = "Config file not valid"

def get_metric_info(url: str):
    """Check website availability and retrieve information.
    
    Param:
        url (str): address of the website to check
        
    Return:
        (dict): information retrieved from the website check:
            - ts (datetime): exact moment of the check
            - url (str): url requested
            - time (float): time for the website responce
            - status (int): status code from the website
            - body (unicode): html body from the website
            - error (str): an error description if something go wrong
    """
    
    ts = str(datetime.now())
    
    try:
        start = time.time()
        r = requests.get(url)
        end = time.time()
        status = r.status_code
        body = r.text[:50]
        error = ""
        
    except Exception as e:
        end = time.time()
        status = -1
        body = ""
        error = "Server unreachable"
    
    return {
        "ts": ts,
        "url": url,
        "time": end - start,
        "status": status,
        "body": body,
        "error": error
        }


def main(argv: list = None):
    """Main function for the application."""
    
    
    opt = option.AppOption()
    
    if(opt.parse()):
        return ReturnCode.OPTION_PARSER_ERROR
    
    try:
        url_list = config.UrlList(opt)
    
    except Exception as e:
        print(ERROR_URL_LIST_FILE_NOT_VALID)
        return ReturnCode.URL_LIST_FILE_NOT_VALID_ERROR
    
    try:
        cfg = config.AppConfig(opt)
    
    except Exception as e:
        print(ERROR_CONFIG_FILE_NOT_VALID)
        return ReturnCode.CONFIG_FILE_NOT_VALID_ERROR
    
    while(True):
        try:
            # Create the producer basd on the config file parameters
            producer = KafkaProducer(
                bootstrap_servers = cfg['kafka']['server_address'],
                security_protocol = "SSL",
                ssl_cafile = cfg['kafka']['ssl_cafile'],
                ssl_certfile = cfg['kafka']['ssl_certfile'],
                ssl_keyfile = cfg['kafka']['ssl_keyfile'])
            
            # Test all the urls in the list
            for url in url_list.url_list:
                metric = json.dumps(get_metric_info(url), indent = 2)
                print(metric)
                print("Sending to Kafka...", end = '')
                producer.send(cfg['kafka']['topic_name'], metric.encode("utf-8"))
                print("OK")
                time.sleep(float(opt.pause))
            
            # Force sending of all messages
            producer.flush()
    
            time.sleep(float(opt.sleep_time))
        
        except KeyboardInterrupt:
            break
        
    return ReturnCode.OK

