```bash

sam build

sam deploy --guided --stack-name stream-s3-to-es --region us-east-1 --profile officity

sam local invoke "StreamDataFunction" \
    -e events/event.json \
    --region us-east-1 --profile officity
```