git rev-parse HEAD > app/uix/revision.txt
docker build . --no-cache -t tracardi/com-microservice:0.8.0-dev
docker push tracardi/com-microservice:0.8.0-dev