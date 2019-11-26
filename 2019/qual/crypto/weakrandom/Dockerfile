FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd python3.7 python3.7-dev && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m weakrandom && mkdir -p /home/weakrandom

RUN chown -R root:weakrandom /home/weakrandom && chmod 750 /home/weakrandom

CMD /usr/bin/startchall
