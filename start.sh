#!bin/bash
docker build --no-cache -t dynamsoft . && docker run --name dynamsoft -e DYNAMSOFT_LICENSE=$DYNAMSOFT_LICENSE -p 5000:5000 dynamsoft
