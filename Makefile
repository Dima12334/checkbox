up:
	docker-compose up

up-with-build:
	docker-compose up --build

down:
	docker-compose down

test:
	docker-compose exec app pytest tests
