# MediAlert — Makefile
# Usage: make <target>

.PHONY: install setup run test clean

install:
	pip install -r requirements.txt

setup:
	python setup.py
	python scripts/setup_database.py

run:
	python main.py

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
