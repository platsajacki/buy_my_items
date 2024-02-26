lint:
	python3 bmi/manage.py check
	flake8 .
	mypy .
