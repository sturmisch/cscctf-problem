FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m babyprintf && mkdir -p /home/babyprintf

RUN chown -R root:babyprintf /home/babyprintf && chmod 750 /home/babyprintf

CMD /usr/bin/startchall