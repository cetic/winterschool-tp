#!/bin/bash

docker --version > /dev/null
if [ $? -eq  0 ] ; 
    then docker build -f sender.dockerfile -t sender:latest . && \
    docker build -f receiver.dockerfile -t receiver:latest . && \
    docker build -f fuzzer.dockerfile -t fuzzer:latest . ; 
    else echo "Install docker and add your user to the docker group to build the TP." ; 
fi

docker-compose --version > /dev/null
if [ $? -eq  0 ] ; 
    then docker-compose up -d ; 
    else echo "Install docker-compose to start the TP." ; 
fi
