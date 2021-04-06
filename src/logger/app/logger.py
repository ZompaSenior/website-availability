# -*- coding: utf-8 -*-

"""Description of the module."""

# Std Import
from datetime import datetime
import json
import requests
import time
import enum

# Site-package Import
from kafka import KafkaConsumer

# Project Import
from logger.util import config
from logger.util import db
from logger.util import option


class ReturnCode(enum.IntEnum):
    OK = 0
    OPTION_PARSER_ERROR = enum.auto()
    URL_LIST_FILE_NOT_VALID_ERROR = enum.auto()
    CONFIG_FILE_NOT_VALID_ERROR = enum.auto()
    

ERROR_URL_LIST_FILE_NOT_VALID = "Url list file not valid"
ERROR_CONFIG_FILE_NOT_VALID = "Config file not valid"


def main(argv: list = None):
    """Main function for the application."""
    
    
    opt = option.AppOption()
    
    if(opt.parse()):
        return ReturnCode.OPTION_PARSER_ERROR
    
    try:
        cfg = config.AppConfig(opt)
    
    except Exception as e:
        print(ERROR_CONFIG_FILE_NOT_VALID)
        return ReturnCode.CONFIG_FILE_NOT_VALID_ERROR
    
    print("Creating Consumer ...", end = '')
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
    
    print("OK")
    
    app_db = db.AppDB(cfg)
    
    while(True):
        try:
            print(".", end = '')
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

            time.sleep(float(opt.sleep_time))
        
        except KeyboardInterrupt:
            break
        
    return ReturnCode.OK
