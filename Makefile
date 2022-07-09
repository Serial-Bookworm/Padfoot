build:
	docker compose up --build -d --remove-orphans

up:
	docker compose up -d

down:
	docker compose down

show_logs:
	docker compose logs

migrate:
	docker compose exec web python padfoot_src/manage.py migrate

makemigrations:
	docker compose exec web python padfoot_src/manage.py makemigrations

collectstatic:
	docker compose exec web python padfoot_src/manage.py collectstatic --no-input --clear

superuser:
	docker compose exec web python padfoot_src/manage.py createsuperuser

down-v:
	docker compose down -v