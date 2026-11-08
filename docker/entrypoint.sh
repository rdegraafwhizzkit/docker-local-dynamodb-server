#!/bin/bash

cd /opt/dynamodb

exec java -cp "local-dynamodb-server-${dynamodb_version}.jar:$(cat classpath)" \
  -Dsqlite4java.library.path=./ \
  LocalDynamoDBServer \
  -sharedDb \
  -optimizeDbBeforeStartup \
  -dbPath ./