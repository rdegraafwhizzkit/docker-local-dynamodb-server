#!/bin/bash

cd /opt/dynamodb

exec java -cp "local-dynamodb-server-${dynamodb_version}.jar:$(cat classpath)" \
  -Dsqlite4java.library.path=/root/.m2/repository/com/almworks/sqlite4java/libsqlite4java-linux-amd64/${sqlite4java_version}/ \
  LocalDynamoDBServer \
  -sharedDb \
  -optimizeDbBeforeStartup \
  -dbPath ./