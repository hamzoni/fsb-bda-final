#!/usr/bin/bash

cat test.csv | python map.py
cat test.csv | python map.py | python reduce.py
cat test.csv | python mapper.py | python reducer.py

# ON HADOOP cluster
hadoop-streaming -files s3://fsb-emr-scripts/mapper.py,s3://fsb-emr-scripts/reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input s3://fsb-bigdata-input/01d5d495-3626-46ae-8b3c-14ff70706274.csv -output s3://fsb-bigdata-output/results

hadoop-streaming -files s3://fsb-emr-scripts/mapper.py,s3://fsb-emr-scripts/reducer.py \
  -mapper mapper.py -reducer reducer.py \
  -input s3://fsb-bigdata-input/01d5d495-3626-46ae-8b3c-14ff70706274.csv \
  -output s3://fsb-bigdata-output/results


hadoop-streaming -files s3://fsb-emr-scripts/mapper.py,s3://fsb-emr-scripts/reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input s3://fsb-bigdata-input/*.csv -output s3://fsb-bigdata-output/results4

hadoop-streaming -files s3://fsb-emr-scripts/mapper.py,s3://fsb-emr-scripts/reducer.py \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -input s3://fsb-bigdata-input/*.csv -output s3://fsb-bigdata-output/results3

# upload lambda zip
rm elasticsearch-lambda.zip
zip -r elasticsearch-lambda.zip ./elasticsearch-lambda
aws lambda update-function-code --function-name push-to-es --zip-file fileb://elasticsearch-lambda.zip --profile officity
