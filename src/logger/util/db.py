# -*- coding: utf-8 -*-

"""Database utility collection."""

# Std Import
from datetime import datetime

# Site-package Import
import postgresql.driver

# Project Import
from util import config


class AppDB():
    """Utility for all db management functinality."""
    
    SQL_SEARCH_URL = "SELECT id FROM monitored_url WHERE url = $1"
    SQL_INSERT_URL = "INSERT INTO monitored_url (url) VALUES ($1)"
    SQL_INSERT_METRIC = """INSERT INTO metric
        (url_id, ts, response_time, status, count_matches, error)
        VALUES ($1, $2, $3, $4, $5, $6)"""

    SQL_SEARCH_TABLE_MONITORED_URL = """
    SELECT
        table_name
    FROM
        information_schema.tables
    WHERE
        table_name = 'monitored_url' AND
        table_schema = 'public'
    """

    SQL_SEARCH_TABLE_METRIC = """
    SELECT
        table_name
    FROM
        information_schema.tables
    WHERE
        table_name = 'metric' AND
        table_schema = 'public'
    """
    
    SQL_CREATION_TABLE_MONITORED_URL = """
    CREATE TABLE monitored_url(
        id    SERIAL PRIMARY KEY,
        url   TEXT NOT NULL
        )
    """
    
    SQL_CREATION_TABLE_METRIC = """
    CREATE TABLE metric(
        id              SERIAL PRIMARY KEY,
        url_id          integer NOT NULL references monitored_url(id),
        ts              timestamp NOT NULL,
        response_time   real NOT NULL,
        status integer  NOT NULL,
        count_matches   integer NOT NULL,
        error           character varying (100) NOT NULL
        )
    """
    
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
        
        # Call the function to initialize the needed tables
        self.migration()
        
    def migration(self):
        """Create db tables if not present."""
        
        with self.C() as db:
            print("Checking 'monitored_url' table ...")
            ps = db.prepare(self.SQL_SEARCH_TABLE_MONITORED_URL)
            rows = ps()
            
            if(rows):
                print("Present")
            
            else:
                print("Not present, creating ...")
                db.execute(self.SQL_CREATION_TABLE_MONITORED_URL)
                print("OK")

            print("Checking 'metric' table ...")
            ps = db.prepare(self.SQL_SEARCH_TABLE_METRIC)
            rows = ps()
            
            if(rows):
                print("Present")
                
            else:
                print("Not present, creating ...")
                db.execute(self.SQL_CREATION_TABLE_METRIC)
                print("OK")
    
    def get_url_id(self, url: str, db):
        """Utility to check table presence in the database.
        
        Param:
            url (str): url to search the id
        
        """
        
        print("Searching url in cache ...")
        tmp_id = self.__url_ids.get(url, 0)
        
        if(tmp_id):
            print("Found")
            
        else:
            print("Not found, searching on db ...")
            
            # We are going to have two round:
            # 1. Search ro the url, stop if found or created otherwise
            # 2. In this case we have created a new url, so search for its id
            for i in range(2):
                ps = db.prepare(self.SQL_SEARCH_URL)
                rows = ps(url)
                
                if(rows):
                    tmp_id = rows[0][0]
                    self.__url_ids[url] = tmp_id
                    print(f"Url id = {tmp_id}")
                    break
                    
                else:
                    print("url not found, creating ...")
                    pi = db.prepare(self.SQL_INSERT_URL)
                    e = pi(url)
                    print("OK")
        
        # Returning found url id
        return tmp_id
    
    def insert_metric(self, metric: dict):
        """Insert metric information in the 'metric' table.
        
        Param:
            metric (dict): dictionary containing the metric information.
        
        Example:
        
        An example of metric information dict:
            {
                "ts": "2021-04-11 22:28:39.025829",
                "url": "https://www.python.org/",
                "response_time": 0.21059155464172363,
                "status": 200,
                "count_matches": 1,
                "error": ""
            }
        
            """
        
        with self.C() as db:
            # This part could be managed with a transaction, but I'm assuming
            # only one instance of Logger is running at a time
            pi = db.prepare(self.SQL_INSERT_METRIC)
            url_id = self.get_url_id(metric['url'], db)
            
            print("Inserting new 'metric' ...")
            e = pi(url_id,
                   datetime.strptime(metric['ts'], '%Y-%m-%d %H:%M:%S.%f'),
                   metric['response_time'],
                   metric['status'],
                   metric['count_matches'],
                   metric['error'])
            
            print("OK")
    
    