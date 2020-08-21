# A Docker image for a local development DynamoDB Server
This is a set of files that build a Docker image for a DynamoDB development server.

# Instructions
You may find the latest version of the DynamoDBLocal jars by invoking:
```
aws s3 ls s3://dynamodb-local-frankfurt/release/com/amazonaws/DynamoDBLocal --recursive|grep "\.jar$"|rev|cut -d "/" -f 1|rev
```
In Dockerfile.dynamodb version 1.12.0 is used.

## Build the base JDK8 image
```
docker build --no-cache -t jdk8 -f Dockerfile.jdk8 .
```

## Build the DynamoDB image
```
docker build --no-cache -t "dynamodb:1.12.0" -f Dockerfile.dynamodb .
```

# Start a container from this image
```
docker run -d -p 8000:8000 dynamodb:1.12.0
```

## Browse to the DynamoDB shell
Navigate to http://localhost:8000/shell

## Run the Python example code
```
python3 dynamodb-test.py
```
