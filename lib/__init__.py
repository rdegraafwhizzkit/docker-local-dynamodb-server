import boto3
from botocore.exceptions import ClientError


class DynamoDBTable:
    class Exception(Exception):
        pass

    def __init__(self, table_name, client):
        self.table_name = table_name
        self.client = client or boto3.client('dynamodb')

    def delete_table(self):
        try:
            self.client.delete_table(TableName=self.table_name)
        except ClientError as ignored:
            pass

    def create_table(self, attribute_definitions: list, key_schema: list, provisioned_throughput: dict | None = None):
        try:
            self.client.create_table(
                TableName=self.table_name,
                AttributeDefinitions=attribute_definitions,
                KeySchema=key_schema,
                ProvisionedThroughput=provisioned_throughput or {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        except ClientError as ignored:
            pass

    def update_attributes(self, item) -> dict:
        return item

    def put_item(self, item: dict, **kwargs):
        item = self.update_attributes(item)
        self.client.put_item(
            TableName=self.table_name,
            Item=item,
            **kwargs
        )
