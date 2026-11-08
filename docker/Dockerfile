FROM debian:bookworm

ARG dynamodb_version=1.12.0
ARG sqlite4java_version=1.0.392

ENV dynamodb_version=$dynamodb_version
ENV sqlite4java_version=$sqlite4java_version
ENV JAVA_HOME=/usr

EXPOSE 8000

WORKDIR /opt/dynamodb

RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless maven

COPY pom.xml /opt/dynamodb/
COPY LocalDynamoDBServer.java /opt/dynamodb/src/main/java/LocalDynamoDBServer.java

RUN mvn -q clean package -Ddynamodb.version=$dynamodb_version -Dsqlite4java.version=$sqlite4java_version && \
    mvn -q dependency:build-classpath \
      -Dmdep.outputFile=classpath \
      -Ddynamodb.version=$dynamodb_version \
      -Dsqlite4java.version=$sqlite4java_version && \
    cp -f target/*jar ./ && \
    rm -rf target

COPY entrypoint.sh ./
COPY sqlite4java.sh ./

RUN chmod 755 entrypoint.sh sqlite4java.sh
RUN ./sqlite4java.sh

ENTRYPOINT [ "/opt/dynamodb/entrypoint.sh" ]
