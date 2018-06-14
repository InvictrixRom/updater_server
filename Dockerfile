FROM python:2.7

COPY . /app
COPY builds /var/www/html/builds
WORKDIR /app

ENV FLASK_APP "app.py"
RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn -b 0.0.0.0:5000 -w 4 app:app
