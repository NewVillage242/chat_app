docker-build:
	docker image rm go-backend | true
	docker build -t go-backend .
docker-run:
	docker container stop go-go | true
	docker run --rm -d --name go-go -p 8000:5000 -it go-backend /bin/sh

docker-ssh:
	docker exec -it go-go /bin/sh

compose-up:
	docker compose up || docker-compose up

compose-down:
	docker compose down || docker-compose down

compose-watch:
	docker compose watch || docker-compose watch
