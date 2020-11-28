```bash

aws cloudformation create-stack \
    --stack-name iot-analytics-fsb \
    --template-body file://cloudformation/iot-analytics.yaml \
    --parameters ParameterKey=ProjectName,ParameterValue=iot-analytics-demo \
               ParameterKey=IoTTopicName,ParameterValue=iot-device-data \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile officity

```