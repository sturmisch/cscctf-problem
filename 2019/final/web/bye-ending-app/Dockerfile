FROM python:3.7.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir /app

RUN apt-get -y update
RUN apt-get install dbus-x11 packagekit-gtk3-module libcanberra-gtk-module xvfb gtk2-engines-pixbuf zlib1g-dev xvfb libxcomposite1 libasound2 libdbus-glib-1-2 libgtk2.0-0 -y
RUN apt-get install fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 curl unzip wget xvfb -y

# ENV DISPLAY=:0

# install firefox and geckodriver
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install -r /app/requirements.txt

RUN mkdir -p /var/log/challenges/

COPY challs.conf /etc/supervisor/challs.conf

EXPOSE 8000

# ENTRYPOINT ["/usr/local/bin/xvfb-run"]
CMD ["supervisord", "-c", "/etc/supervisor/challs.conf"]
