#!/bin/bash

sudo cp logger.service /etc/systemd/system/

cd ../../src/logger

docker build --tag website-availability-logger .

sudo systemctl enable logger