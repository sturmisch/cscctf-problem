FROM python:3.7.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "admin.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

RUN mkdir /app
WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install -r requirements.txt

EXPOSE 80

CMD flask run --host=127.0.0.1 --port=80
