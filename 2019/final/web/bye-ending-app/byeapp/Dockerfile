FROM python:3.7.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "byee.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir /app

# RUN sed -i 's/http/ftp/' /etc/apt/sources.list

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install -r /app/requirements.txt

EXPOSE 9000

CMD flask run --host=0.0.0.0 --port=9000
