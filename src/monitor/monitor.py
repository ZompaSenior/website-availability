# -*- coding: utf-8 -*-

"""Description of the module."""

# Std Import

# Site-package Import

# Project Import

from datetime import datetime
import json
import requests
import time

def get_metric_info(url):
    """
    """
    
    start = time.time()
    ts = str(datetime.now())
    
    try:
        r = requests.get(url)
        status = r.status_code
        body = r.text[:100]
    except Exception as e:
        status = -1
        body = f"Server unreachable"
    
    end = time.time()

    return {
        "url": url,
        "ts": ts,
        "status": status,
        "body": body
        }

server_list = [
    "http://www.google.com",
    "https://www.python.org/pippo",
    "http://www.xyzhhhggffdd.com"
    ]

for url in server_list:
    print(json.dumps(get_metric_info(url), indent = 2))