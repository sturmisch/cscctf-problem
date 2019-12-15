FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install php7.0 apache2 libapache2-mod-php -y

RUN a2enmod php7.0

WORKDIR /var/www/html
COPY . /var/www/html
RUN rm -f index.html
RUN rm -f get_your_ans_here
RUN rm -f Dockerfile
RUN rm -f docker-compose.yml

RUN chmod 777 /var
RUN chmod 777 /var/log
RUN chmod 777 /var/log/apache2
RUN chmod 777 /var/log/apache2/access.log
#RUN chown root:www-data get_your_ans_here
#RUN chmod 444 get_your_ans_here
#RUN chown root:www-data *
#RUN chown root:www-data /var
#RUN chown root:www-data /var/log
#RUN chown root:www-data /var/log/apache2
#RUN chown root:www-data /var/log/apache2/access.log

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND
