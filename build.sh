git rev-parse HEAD > app/uix/revision.txt
docker build . --no-cache -t tracardi/com-microservice:0.8.2.1
docker push tracardi/com-microservice:0.8.2.1