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
docker build --platform linux/amd64    -t "dynamodb:x86_64"   -f Dockerfile .
docker build --platform linux/arm64/v8 -t "dynamodb:arm64-v8" -f Dockerfile .
```

# Start a container from this image
```
docker container rm dynamodb
docker run --rm -p 8000:8000 --name dynamodb dynamodb:x86_64
docker run --rm -p 8000:8000 --name dynamodb dynamodb:arm64-v8
docker run -d -p 8000:8000   --name dynamodb dynamodb:arm64-v8
```

## Browse to the DynamoDB shell
Navigate to http://localhost:8000/shell

## Set up
```
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip pip-tools

pip-compile dev-requirements.in
pip-compile requirements.in

pip install --upgrade -r dev-requirements.txt 
pip install --upgrade -r requirements.txt
```

## Run the Python example code
```
ENDPOINT_URL=http://192.168.1.220:8000 python3 tests.py
```
