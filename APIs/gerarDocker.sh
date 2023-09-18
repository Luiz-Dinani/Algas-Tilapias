python3 atualizarAWSCredentials.py

docker stop samaka-api-ct
docker rm samaka-api-ct

docker image rm samaka-api-img
docker image build -t samaka-api-img .

docker container run --name samaka-api-ct -p 5000:5000 -d --restart unless-stopped samaka-api-img
docker start samaka-api-ct
