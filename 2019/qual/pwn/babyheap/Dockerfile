FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m babyheap && mkdir -p /home/babyheap

RUN chown -R root:babyheap /home/babyheap && chmod 750 /home/babyheap

CMD /usr/bin/startchall
