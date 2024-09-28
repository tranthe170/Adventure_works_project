# Makefile for managing Docker-based services

.PHONY: start stop restart reset

start:
	@echo "Starting all services..."
	@docker build -t hadoop-base docker/hadoop/hadoop-base
	@docker build -t hive-base docker/hive/hive-base
	@docker build -t spark-base docker/spark/spark-base
	@docker-compose up -d --build

stop:
	@echo "Stopping all services..."
	@docker-compose down

restart: stop start
	@echo "Restarting all services..."

reset:
	@echo "WARNING: Resetting everything! This will remove all containers, networks, volumes, and images."
	@docker-compose down
	@docker system prune -f
	@docker volume prune -f
	@docker network prune -f
	@rm -rf ./mnt/postgres/*
	@docker rmi -f $$(docker images -a -q)
