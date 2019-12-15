FROM ubuntu:16.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m childrenheap && mkdir -p /home/childrenheap

RUN chown -R root:childrenheap /home/childrenheap && chmod 750 /home/childrenheap

CMD /usr/bin/startchall