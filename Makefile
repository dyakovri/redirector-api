prod-up:
	docker-compose --file docker-compose.prod.yml up --detach --remove-orphans --force-recreate --build
	docker-compose --file docker-compose.prod.yml run --rm api bash -c 'alembic upgrade head'

prod-down:
	docker-compose --file docker-compose.prod.yml down
