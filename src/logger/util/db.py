# -*- coding: utf-8 -*-

"""Database utility collection."""

# Std Import

# Site-package Import
import postgresql

# Project Import

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

def check_table_presence(sql):
    db = postgresql.open('pq://user:password@host:port/database')
    