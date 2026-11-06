# A Docker image for a local development DynamoDB Server
This is a set of files that build a Docker image for a DynamoDB development server.

# Instructions
You may find the latest version of the DynamoDBLocal jars by invoking:
```
aws s3 ls s3://dynamodb-local-frankfurt/release/com/amazonaws/DynamoDBLocal --recursive|grep "\.jar$"|rev|cut -d "/" -f 1|rev
```
In Dockerfile version 1.12.0 is used.

## Build the DynamoDB image
```
docker builder prune -a -f
cd docker
docker build --platform linux/amd64 -t "dynamodb" -f Dockerfile .
```

# Start a container from this image
```
docker container rm dynamodb
docker run --rm -p 8000:8000 dynamodb
```

## Browse to the DynamoDB shell
Navigate to http://localhost:8000/shell


## Set up
```
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
```

## Run the Python example code
```
python3 tests.py
```
