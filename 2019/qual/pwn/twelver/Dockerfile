FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m twelver && mkdir -p /home/twelver

RUN chown -R root:twelver /home/twelver && chmod 750 /home/twelver

CMD /usr/bin/startchall
