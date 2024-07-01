# Базовый образ
FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["python", "/code/programmer_library/manage.py", "migrate", "runserver", "0.0.0.:8000"]
