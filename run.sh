#!/bin/bash

cd $(dirname $0)
source bin/activate
./run.py
deactivate
