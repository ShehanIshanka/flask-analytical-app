venv:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip

.PHONY: setup
setup: venv
	./venv/bin/pip3 install -r requirements.txt

.PHONY: run
run:
	./venv/bin/python3 -m src.app

.PHONY: setup-test
setup-test: venv setup
	./venv/bin/pip3 install -r requirements-test.txt
	./venv/bin/playwright install

.PHONY: setup-style
setup-style: venv setup
	./venv/bin/pip3 install --no-cache-dir -r requirements-style.txt

.PHONY: setup-dev
setup-dev: setup setup-test setup-style

.PHONY: check_format
check_format: #check which files will be reformatted
	./venv/bin/black --check .

.PHONY: format
format: #format files
	./venv/bin/black .

.PHONY: lint
lint:
	./venv/bin/flake8 .

.PHONY: clean-app
clean-app:
	rm -rf app-data venv
