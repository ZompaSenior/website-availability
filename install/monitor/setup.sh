#!/bin/bash

sudo cp monitor.service /etc/systemd/system/

cd ../../src/monitor

docker build --tag website-availability-monitor .

sudo systemctl enable monitor