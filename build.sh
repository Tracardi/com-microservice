git rev-parse HEAD > app/uix/revision.txt
docker build . --no-cache -t tracardi/tracardi-microservice:0.7.2-dev