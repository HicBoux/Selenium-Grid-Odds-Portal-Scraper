all: build up

build:
	docker-compose -f docker-compose.yml build 
up:
	docker-compose -f docker-compose.yml up -d

start:
	docker-compose -f docker-compose.yml start 
down:
	docker-compose -f docker-compose.yml down 
destroy:
	docker-compose -f docker-compose.yml down -v 
stop:
	docker-compose -f docker-compose.yml stop 
restart:
	docker-compose -f docker-compose.yml stop 

.PHONY: all verbose build up start down destroy stop restart 