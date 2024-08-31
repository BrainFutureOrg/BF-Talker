VENV = ./venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
APP = ./src/main.py

run:
	 $(PYTHON)	 $(APP)

update: requirements.txt
	 $(PIP) install -r requirements.txt


setup: requirements.txt
	 python3 -m venv $(VENV)
	 $(PIP) install -r requirements.txt


clean:
	 rm -rf __pycache__
	 rm -rf $(VENV)