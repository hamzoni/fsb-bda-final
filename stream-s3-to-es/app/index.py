#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-aws-integrations.html
# https://stackoverflow.com/questions/25908484/how-to-fix-read-timed-out-in-elasticsearch
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html

import boto3
import requests
from requests_aws4auth import AWS4Auth
import os
import uuid
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers

AWS_REGION = os.environ['ES_REGION']
AWS_SERVICE = 'es'
credentials = boto3.Session().get_credentials()
AWS4_AUTH = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    AWS_REGION, AWS_SERVICE,
    session_token=credentials.token
)

ES_HOST = os.environ['ES_HOST']
ES_INDEX = 'iot'
ES_TYPE = '_doc'
ES_URL = f'{ES_HOST}/{ES_INDEX}/{ES_TYPE}'

HEADERS = {
    'Content-Type': 'application/json'
}

AWS_S3 = boto3.client('s3')

ES = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': 443}],
    http_auth=AWS4_AUTH,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=300
)


def prepare_document(line: str):
    columns = [
        str(col).replace('\"', '').replace('b\'', '')
        for col in line.strip().split(',')
    ]

    device_name = columns[0]
    humidity = columns[2]
    temperature = columns[3]
    received_at = columns[9]

    try:
        return {
            'device_name': device_name,
            'received_at': received_at,
            'humidity': float(humidity),
            'temperature': float(temperature),
        }
    except:
        return None


def get_lines(record):
    global AWS_S3
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    obj = AWS_S3.get_object(Bucket=bucket, Key=key)
    body = obj['Body'].read()
    return body.splitlines()


def parse_record(record):
    global ES_URL, AWS4_AUTH, HEADERS, ES_TYPE, ES_INDEX

    documents = [prepare_document(str(line)) for line in get_lines(record)]
    documents = list(filter(lambda doc: doc is not None, documents))

    actions = [
        {
            '_id': str(uuid.uuid4()),
            'doc_type': ES_TYPE,
            'doc': doc
        } for doc in documents
    ]
    
    print(f'Indexing total of {len(actions)} documents')

    try:
        response = helpers.bulk(ES, actions, index=ES_INDEX, doc_type=ES_TYPE)
        print('\nRESPONSE:', response)
    except Exception as e:
        print('\nERROR:', e)


def handler(event, context):
    for record in event['Records']:
        parse_record(record)
