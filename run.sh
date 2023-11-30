#!/bin/bash
source ".venv/bin/activate"
# rm -rf queues/*
python -u scripts/executor.py --filepath=nodes/n1.py &
python -u input-data.py