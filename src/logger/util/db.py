# -*- coding: utf-8 -*-

"""Database utility collection."""

# Std Import

# Site-package Import
import postgresql.driver

# Project Import
from logger.util import config
from datetime import datetime

TABLE_MONITORED_URL_CREATION_SQL = """CREATE TABLE monitored_url(
   id  SERIAL PRIMARY KEY,
   url           TEXT      NOT NULL,
);"""

TABLE_METRIC_CREATION_SQL = """CREATE TABLE metric(
   id  SERIAL PRIMARY KEY,
   url_id  integer      NOT NULL,
   ts timestamp  NOT NULL
   time real  NOT NULL
   status integer  NOT NULL
   error character varying (100)  NOT NULL
);"""

TABLE_MONITORED_URL_PRESENCE_SQL = """SELECT table_name
FROM
    information_schema.tables
WHERE
    table_name = 'monitored_url' AND
    table_schema = 'public';"""

TABLE_METRIC_PRESENCE_SQL = """SELECT table_name
FROM
    information_schema.tables
WHERE
    table_name = 'metric' AND
    table_schema = 'public';"""

class AppDB():
    """Utility for all db management functinality."""
    
    SQL_SEARCH_URL = "SELECT id FROM monitored_url WHERE url = $1"
    SQL_INSERT_URL = "INSERT INTO monitored_url (url) VALUES ($1)"
    SQL_INSERT_METRIC = """INSERT INTO metric (url_id, ts, time, status, error)
        VALUES ($1, $2, $3, $4, $5)"""
    
    def __init__(self, app_config: config.AppConfig):
        """Class constructor.
        
        Param:
            app_config (AppConfig): configuration file parameters
        """
        
        self.C = postgresql.driver.default.host(
            host = app_config["postgresql"]["host"],
            user = app_config["postgresql"]["user"],
            password = app_config["postgresql"]["password"],
            database = app_config["postgresql"]["database"],
            port = int(app_config["postgresql"]["port"]),
            sslmode = app_config["postgresql"]["sslmode"])#,
            #sslcrtfile = app_config["postgresql"]["sslcrtfile"])
        
        # Dictionary of the url's id, initialized
        self.__url_ids = {}
        
    def get_url_id(self, url: str):
        """Utility to check table presence in the database.
        
        Param:
            url (str): url to search the id
        
        """
        
        tmp_id = self.__url_ids.get(url, 0)
        
        if(not tmp_id):
            for i in range(2):
                with self.C() as db:
                    ps = db.prepare(self.SQL_SEARCH_URL)
                    rows = ps(url)
                    
                    if(rows):
                        tmp_id = rows[0][0]
                        self.__url_ids[url] = tmp_id
                        break
                        
                    else:
                        pi = db.prepare(self.SQL_INSERT_URL)
                        e = pi(url)
                        print(e)
        
        return tmp_id
    
    def insert_metric(self, metric: dict):
        with self.C() as db:
            pi = db.prepare(self.SQL_INSERT_METRIC)
            url_id = self.get_url_id(metric['url'])
            e = pi(url_id,
                   datetime.strptime(metric['ts'], '%Y-%m-%d %H:%M:%S.%f'),
                   metric['time'],
                   metric['status'],
                   metric['error'])
            
            print(e)
    
if(__name__ == "__main__"):
    
    
    app_db = AppDB()
    