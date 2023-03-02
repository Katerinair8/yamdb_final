FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt --no-cache-dir

RUN apt-get autoremove -y gcc

COPY . ./

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
