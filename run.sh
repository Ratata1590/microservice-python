#!/bin/bash

docker run -dit --rm \
-v $(pwd)/nodes/n1.py:/workspace/n2.py \
-v $(pwd)/queues/:/workspace/queues \
-e FILEPATH=n2.py \
py-microservice:latest

docker run -dit --rm \
-v $(pwd)/input-data.py:/workspace/input-data.py \
-v $(pwd)/input-data.sh:/entrypoint.sh \
-v $(pwd)/queues/:/workspace/queues \
py-microservice:latest