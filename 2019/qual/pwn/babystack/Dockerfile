FROM ubuntu:18.04

RUN dpkg --add-architecture i386
RUN apt-get update && apt-get install -y xinetd libc6:i386 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m babystack && mkdir -p /home/babystack

RUN chown -R root:babystack /home/babystack && chmod 750 /home/babystack

CMD /usr/bin/startchall