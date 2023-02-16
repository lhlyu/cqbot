#!/bin/sh

docker build -t bot .
docker run -itd --name bot bot python bot.py
docker logs -f bot