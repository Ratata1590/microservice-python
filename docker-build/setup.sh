#!/bin/sh
apk update
apk upgrade --no-cache
apk add python3-dev py3-pip
pip install -r requirements.txt --no-cache-dir
rm requirements.txt setup.sh
mkdir queues