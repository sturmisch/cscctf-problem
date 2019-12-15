FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m maps && mkdir -p /home/maps

RUN chown -R root:maps /home/maps && chmod 750 /home/maps

CMD /usr/bin/startchall