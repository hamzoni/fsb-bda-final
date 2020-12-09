#!/bin/bash

INPUT_BUCKET_NAME='s3://iot-analytics-fsb-datasetoutputbucket-13qgee5qpd786'
OUTPUT_BUCKET_NAME='s3://fsb-bigdata-input'

#aws s3 sync s3://iot-analytics-fsb-datasetoutputbucket-13qgee5qpd786 \
#  s3://fsb-bigdata-input \
#   --include "*.csv" --exclude "*" \
#  --profile officity

INPUT_DIR='input'
OUTPUT_DIR='output'

#rm -rf $INPUT_DIR
#mkdir $INPUT_DIR
#
#rm -rf $OUTPUT_DIR
#mkdir $OUTPUT_DIR
#
aws s3 sync $INPUT_BUCKET_NAME/ $INPUT_DIR --profile officity

find $INPUT_DIR -type f -name \*.csv  -exec cp {} $OUTPUT_DIR \;

aws s3 sync $OUTPUT_DIR $OUTPUT_BUCKET_NAME/ --profile officity
# final mapping fields

#device_name
#last_received_at
#first_received_at
#temperature_highest
#temperature_lowest
#temperature_average
#humidity_highest
#humidity_lowest
#humidity_average
