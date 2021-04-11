# -*- coding: utf-8 -*-

"""Here is the main process of the application."""

# Std Import
from datetime import datetime
import json
import requests
import time
import enum

# Site-package Import
from kafka import KafkaConsumer

# Project Import
from util import config
from util import db
from util import option


class ReturnCode(enum.IntEnum):
    """Here is a collection of possible returned code of the application."""
    
    OK = 0
    OPTION_PARSER_ERROR = enum.auto()
    URL_LIST_FILE_NOT_VALID_ERROR = enum.auto()
    CONFIG_FILE_NOT_VALID_ERROR = enum.auto()
    CONSUMER_CREATION_ERROR = enum.auto()
    DATABASE_INITIALIZATION_ERROR = enum.auto()
    

# Constant for error descriptions
ERROR_CONFIG_FILE_NOT_VALID = "Config file not valid"


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
    
    print("Reading configuration ...")
    try:
        cfg = config.AppConfig(opt)
    
    except Exception as e:
        print(ERROR_CONFIG_FILE_NOT_VALID)
        return ReturnCode.CONFIG_FILE_NOT_VALID_ERROR
    
    print("OK")
    
    print("Creating Consumer ...")
    try:
        consumer = KafkaConsumer(
            cfg['kafka']['topic_name'],
            auto_offset_reset="earliest",
            bootstrap_servers = cfg['kafka']['server_address'],
            client_id = cfg['kafka']['client_name'],
            group_id = cfg['kafka']['group_name'],
            security_protocol="SSL",
            ssl_cafile = cfg['kafka']['ssl_cafile'],
            ssl_certfile = cfg['kafka']['ssl_certfile'],
            ssl_keyfile = cfg['kafka']['ssl_keyfile'])
        
    except Exception as e:
        print(e)
        return ReturnCode.CONSUMER_CREATION_ERROR
        
    print("OK")
    
    print("Creating database helper ...")
    try:
        app_db = db.AppDB(cfg)
        
    except Exception as e:
        return ReturnCode.DATABASE_INITIALIZATION_ERROR
    
    print("OK")
    
    # Application main loop
    while(True):
        try:
            print(".", end = '')
            # From Aiven tutorial
            # Call poll twice. First call will just assign partitions for our
            # consumer without actually returning anything
            for _ in range(2):
                raw_msgs = consumer.poll(timeout_ms=1000)
                for tp, msgs in raw_msgs.items():
                    for msg in msgs:
                        print("Received: {}".format(msg.value))
                        msg_dict = json.loads(msg.value.decode('utf-8'))
                        app_db.insert_metric(msg_dict)
            
            # Commit offsets so we won't get the same messages again
            consumer.commit()
            
            # Take a breath between consumptions
            time.sleep(float(opt.sleep_time))
        
        except KeyboardInterrupt:
            # manage Key interrupt for stopping the application 
            break
    
    # Return ok 0 error
    return ReturnCode.OK
