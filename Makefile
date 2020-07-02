start:
	docker-compose up -d
	fd *.py | entr -c python dag_watcher.py

stop:
	docker-compose down --remove-orphans

kill:
	docker-compose down -v --remove-orphans
