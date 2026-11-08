#!/bin/bash

PLATFORM=$(uname -ms)

case ${PLATFORM} in
  "Linux aarch64")
    cp -f /root/.m2/repository/io/github/luneo7/libsqlite4java-linux-aarch64/*/libsqlite4java-linux-aarch64-1.0.392.so ./
    ;;
  "Linux x86_64")
    cp -f /root/.m2/repository/com/almworks/sqlite4java/libsqlite4java-linux-amd64/*/libsqlite4java-linux-amd64-1.0.392.so ./
    ;;
  *)
    echo "Unsupported platform ${PLATFORM}"
    exit 1
    ;;
esac
