FROM amazoncorretto:8-al2023

ARG dynamodb_version=1.12.0
ARG sqlite4java_version=1.0.392

ENV dynamodb_version=$dynamodb_version
ENV sqlite4java_version=$sqlite4java_version
ENV JAVA_HOME=/usr

WORKDIR /opt/dynamodb

COPY entrypoint.sh /opt/dynamodb/
COPY pom.xml /opt/dynamodb/
COPY LocalDynamoDBServer.java /opt/dynamodb/src/main/java/LocalDynamoDBServer.java

RUN dnf -y install maven
RUN cd /opt/dynamodb && \
    mvn -q clean package -Ddynamodb.version=$dynamodb_version -Dsqlite4java.version=$sqlite4java_version && \
    mvn -q dependency:build-classpath \
      -Dmdep.outputFile=classpath \
      -Ddynamodb.version=$dynamodb_version \
      -Dsqlite4java.version=$sqlite4java_version && \
    cp -f target/*jar ./ && \
    rm -rf target && \
    chmod 755 /opt/dynamodb/entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/opt/dynamodb/entrypoint.sh" ]