#!/bin/bash

curl -sSL https://get.docker.com | sh
systemctl enable docker
sudo docker build -t updater-server .
sudo docker run --net=host updater-server
