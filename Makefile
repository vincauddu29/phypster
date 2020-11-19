clean:
	rm -rf src/Models
	rm -rf src/DTOs
	rm -rf src/Repositories
	rm -rf src/Services
	rm -rf src/Mappeurs
	rm -rf src/Ressources
	rm -rf src/Logs
	rm -rf src/Parsers
	rm -rf src/docker
	rm -rf src/Enums
	rm -rf src/Config
	rm -rf Tests
	rm -rf migrations
	rm server.py

generate: clean
	python3 tests.py

test: generate
	docker-compose -f ./src/docker/docker-compose.test.yml down
	docker-compose -f ./src/docker/docker-compose.test.yml up -d
	sleep 15s
	@export FLASK_APP="server.py"; flask db init; flask db migrate; flask db upgrade
	pytest
	docker-compose -f ./src/docker/docker-compose.test.yml down

run:
	@export FLASK_APP="server.py"; flask run

uninstall:
	pip3 uninstall phypster -y
	rm -rf dist/
	rm -rf build/

build:
	python3 setup.py sdist bdist_wheel

install: build uninstall
	pip3 install .