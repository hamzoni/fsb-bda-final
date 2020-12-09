#!/bin/bash

rm -rf dist
mkdir dist
cp -r app/* dist

# install packages
pip install -r app/requirements.txt -t dist

sam build &&
sam local invoke "StreamDataFunction" \
    -e events/event.json \
    --region us-east-1 --profile officity