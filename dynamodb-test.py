import boto3

client = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)

try:
    client.create_table(
        TableName='dynamodb-test',
        AttributeDefinitions=[{
            'AttributeName': 'message',
            'AttributeType': 'S'
        }],
        KeySchema=[{
            'AttributeName': 'message',
            'KeyType': 'HASH'
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except client.exceptions.ResourceInUseException as e:
    pass

print(client.put_item(
    TableName='dynamodb-test',
    Item={'message': {'S': 'Hello!'}},
    ReturnConsumedCapacity='TOTAL'
))

print(client.scan(
    TableName='dynamodb-test',
    ReturnConsumedCapacity='TOTAL'
))
