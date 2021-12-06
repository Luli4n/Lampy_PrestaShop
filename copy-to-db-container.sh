#!/bin/bash

docker cp ./*.sql <pod-name>:/tmp/be_179927.sql

docker cp ./db-dump.sh <pod-name>:/tmp/db-dump.sh

docker exec <pod-name> chmod +x /tmp/db-dump.sh

docker exec <pod-name> /tmp/db-dump.sh

docker exec <pod-name> rm /tmp/be_179927.sql

docker exec <pod-name> rm /tmp/db-dump.sh