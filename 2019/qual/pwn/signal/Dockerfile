FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m signal && mkdir -p /home/signal

RUN chown -R root:signal /home/signal && chmod 750 /home/signal

CMD /usr/bin/startchall
