#!/bin/bash

echo "connect to http://localhost:8091"
docker run -d -p 8091:8091 --rm --name=mofcolorizerinstance mofcolorizer
