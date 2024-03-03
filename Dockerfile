FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY /bmi .

RUN python manage.py collectstatic

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bmi.wsgi"]
