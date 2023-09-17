docker stop samaka-api-ct
docker rm samaka-api-ct

docker rm image samaka-api-img
docker image build -t samaka-api-img .
docker container run --name samaka-api-ct -p 8080:8080 -d --restart unless-stopped samaka-api-img
docker start samaka-api-ct
