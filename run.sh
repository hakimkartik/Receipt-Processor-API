#!/bin/sh

docker build -t receipt-processor .
docker run -p 3000:3000 receipt-processor