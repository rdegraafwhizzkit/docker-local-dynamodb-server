import boto3
from botocore.exceptions import ClientError


class DynamoDBTable:
    class Exception(Exception):
        """
        Custom Exception class
        """
        pass

    def __init__(self, table_name, client):
        """
        Class constructor

        :param table_name: DynamoDB table name
        :param client: Boto3 client
        """
        self.table_name = table_name
        self.client = client or boto3.client('dynamodb')

    def delete_table(self):
        """
        Delete DynamoDB table, ignore if it does not exist
        See https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb/client/delete_table.html

        :return: None
        """
        try:
            self.client.delete_table(TableName=self.table_name)
        except ClientError as ignored:
            pass

    def create_table(self, attribute_definitions: list, key_schema: list, provisioned_throughput: dict | None = None):
        """
        Create DynamoDB table from given attribute_definitions and key_schema
        See https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb/client/create_table.html

        :param attribute_definitions:
        :param key_schema:
        :param provisioned_throughput:
        :return: None
        """
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

    def update_item_attributes(self, item) -> dict:
        """
        Update DynamoDB item attributes

        :param item: 
        :return: dict (the item) 
        """
        return item

    def put_item(self, item: dict, **kwargs):
        """
        See https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb/client/put_item.html

        :param item: 
        :param kwargs: Extra arguments to the put_item method 
        :return: 
        """
        item = self.update_item_attributes(item)
        self.client.put_item(
            TableName=self.table_name,
            Item=item,
            **kwargs
        )
