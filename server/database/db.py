from boto3 import client
from .tables import tables
from typing import Any
from os import getenv

dynamodb: Any = client('dynamodb',
        #  aws_access_key_id=getenv("aws_access_key_id"),
         aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
        #  aws_secret_access_key=getenv("aws_secret_access_key"),
         aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
        #  aws_session_token=getenv("aws_session_token"),
         aws_session_token=getenv("AWS_SESSION_TOKEN"),
        #  region_name=getenv("aws_region_name"))
         region_name=getenv("AWS_REGION"))

def create_tables() -> None:
    try:
        for table in tables:
            dynamodb.create_table(
                TableName=table["TableName"],
                KeySchema=table["KeySchema"],
                AttributeDefinitions=table["AttributeDefinitions"],
                BillingMode="PAY_PER_REQUEST"
            )
    except Exception as e:
        print(f"Error creating tables: {e}")