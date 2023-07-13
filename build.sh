git rev-parse HEAD > app/uix/revision.txt
docker build . --no-cache -t tracardi/com-microservice:0.8.1-rc3
docker push tracardi/com-microservice:0.8.1-rc3