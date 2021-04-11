# website-availability
Monitors website availability over the network and produces metrics about this

Utility is divided in two different applications, named **Monitor** and
**Logger**. Each application can bee executed running the `main.py` with some
command line option and with proper configuration files, for debug purpose,
but here is prepared two Dockerfile, for production with some script to install
them.

## Monitor
This application read a list of website to monitor from a text file, and provide
a JSON of the metrics collected sending them to a Kafka server.

Here and example of the metrics collected:

``` JSON
{
    "ts": "2021-04-11 22:28:39.025829",
    "url": "https://www.python.org/",
    "response_time": 0.21059155464172363,
    "status": 200,
    "count_matches": 1,
    "error": ""
}'
```

### Debug mode
This application can be run from the file `src/monitor/main.py`.

```
usage: main.py [-h] [--sleep_time SLEEP_TIME] [--pause PAUSE]
               url_list config_file

Monitor

positional arguments:
  url_list              path to the file containing the list of url to test
  config_file           Path to the config .ini file

optional arguments:
  -h, --help            show this help message and exit
  --sleep_time SLEEP_TIME
                        time to sleep between each scan in seconds (default 5)
  --pause PAUSE         time to sleep between two url test in seconds (default
                        1)
```

Some example of `url_list` and of `config_file` can be found in `example/monitor` and
also provide here for convenience:

```
# example/monitor/url_list.txt
# List of the url to monitor with the regular expression to search in the body
#
# Form of the file:
# url | regex
#         ^ regula expressione
#     ^ pipe separator
# ^ url to monitor
#
# Comments start with '#'
# Blank lines are ignored
#
https://www.python.org/|<meta name="application-name" content="Python.org">
https://www.python.org/|<meta name="appplication-name" content="Python.org">
https://www.python.org/pippo|No Regex Necessary
http://www.xyzhhhggffdd.com|No Regex Necessary
http://www.xyzkkkggffdd.com
```

```
; example/monitor/monitor.ini
; This file is used by the Monitor side of website availability and must contain
; one section:
; - kafka: this section contain the producer side information necessary to
;       send metric to Kafka service

[kafka]
server_address = <server name>:<port>
ssl_cafile = <path to 'ca.pem' file>
ssl_certfile = <path to 'service.cert' file>
ssl_keyfile = <path to 'service.key' file>
topic_name = <name of the topic to produce>
```

### Install
To prepare and install the Docker container, prepare configuration files and all
certificate files in the `src/monitor/config` folder and after run the script
`install/monitor/setup.sh`.

## Logger
This apllication collect data from a Kafka server and record it to PostgreSQL
server.

### Debug mode
This application can be run from the file `src/logger/main.py`.

```
usage: main.py [-h] [--sleep_time SLEEP_TIME] [--pause PAUSE] config_file

Logger

positional arguments:
  config_file           Path to the config .ini file

optional arguments:
  -h, --help            show this help message and exit
  --sleep_time SLEEP_TIME
                        time to sleep between each scan i seconds
  --pause PAUSE         time to sleep between two url test in seconds
```

Some example of `config_file` can be found in `example/logger` and also provide here
for convenience:

```
; example/logger/monitor.ini
; This file is used by the Logger side of website availability and must contain
; two section:
; - kafka: this section contain the consumer side information necessary to
;       collect metric from Kafka service
; - postresql: this section contain the connection information for the
;       PostgreSQL database, in witch collect the metric information collected
;       from Kafka

[kafka]
server_address = <server name>:<port>
ssl_cafile = <path to 'ca.pem' file>
ssl_certfile = <path to 'service.cert' file>
ssl_keyfile = <path to 'service.key' file>
topic_name = <name of the topic to consume>
client_name = <name of the client>
group_name = <name of the group>

[postgresql]
host = <server name>
user = <db user>
password = <db password>
database = <db name>
port = <server port>
sslmode = <disable / allow / prefer / require>
sslcrtfile = <path to 'ca.pem' file>
```

### Install
To prepare and install the Docker container, prepare configuration files and all
certificate files in the `src/logger/config` folder and after run the script
`install/logger/setup.sh`.

