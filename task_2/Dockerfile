FROM python:3.8.11-slim-buster


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=adv_db
ENV FLASK_APP=run.py

CMD ["bash", "-c", "flask run --host=0.0.0.0"]

