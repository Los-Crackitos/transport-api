#!/bin/sh

pip3 install --proxy"=193.56.47.20:8080" -r requirements.txt

flask run --host=0.0.0.0
