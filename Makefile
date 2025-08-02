run-dev: install-dev
	docker-compose --file ./docker-compose.dev.yml up -d --build --force-recreate --remove-orphans
	sleep 3
	alembic upgrade head


stop-dev:
	docker-compose --file ./docker-compose.dev.yml down -v
