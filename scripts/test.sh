#!/usr/bin/bash

cat test.csv | python map.py
cat test.csv | python map.py | python reducer.py