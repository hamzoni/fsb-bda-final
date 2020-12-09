#!/usr/bin/bash
aws s3 cp mapper.py s3://fsb-emr-scripts --profile officity
aws s3 cp reducer.py s3://fsb-emr-scripts --profile officity
