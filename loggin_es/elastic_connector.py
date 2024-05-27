import os
from elasticsearch import Elasticsearch
from datetime import datetime


ES_CLIENT = Elasticsearch(
  "https://b2df3cb9e1674220b93a11585c454084.westeurope.azure.elastic-cloud.com:443",
  api_key="XXXXXXXXXXXXXXXXXXXXXXXX"
)

FAKE_UUID = "73330bca-9ec9-4569-ba3f-005751b63250"

def log_to_elasticsearch(log_data: dict):
    print(log_data)
    res = ES_CLIENT.index(index="demo-ai-search", body=log_data)
    print(f"Logged to Elasticsearch with result: {res['result']}")
