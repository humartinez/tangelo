FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list && \
    apt-get update && \
    apt-get install -y mongodb-org=4.2.2  mongodb-org-server=4.2.2  mongodb-org-shell=4.2.2 mongodb-org-mongos=4.2.2 mongodb-org-tools=4.2.2&& \
    mkdir -p /data/db

ADD mongodb.conf /etc/mongodb.conf
    

#EXPOSE 27017

#ENTRYPOINT ["/usr/bin/mongod"]
ENTRYPOINT ["/usr/bin/mongod", "--config", "/etc/mongodb.conf"]
