lint:
	python3 bmi/manage.py check
	flake8 .
	mypy .

test:
	pytest --cov=bmi/
