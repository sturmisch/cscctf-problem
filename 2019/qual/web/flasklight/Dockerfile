FROM ubuntu:xenial

RUN apt update -y && apt install -y python-pip python-dev

RUN pip install flask

RUN adduser flasklight

RUN mkdir /flasklight

USER flasklight

ENTRYPOINT ["python"]

CMD ["/flasklight/app.py"]
