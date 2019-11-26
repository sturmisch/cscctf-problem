FROM ubuntu:xenial

RUN apt-get update && apt-get install -y apache2 php7.0
RUN adduser proveyouarenotahuman

RUN mkdir /proveyouarenotahuman && chown root:proveyouarenotahuman /proveyouarenotahuman && chmod 750 /proveyouarenotahuman

USER proveyouarenotahuman

CMD php -S 0.0.0.0:9001 -t /proveyouarenotahuman > /dev/null 2>&1