# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Start from the latest golang base image
FROM golang:latest

# Set the Current Working Directory inside the container
WORKDIR /app

# Put the flag.
COPY Flag /etc/spartan

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# RUN mv Flag /etc/spartan

RUN chmod -R 555 /app

RUN chmod +w /app/storage

# Give some fun limit for the user :)
RUN chmod a-x /bin/cat
RUN chmod a-x /usr/bin/tail
RUN chmod a-x /usr/bin/head
RUN chmod a-x /bin/more
RUN chmod a-x /usr/bin/python
RUN passwd -l root
RUN useradd admin -m -d /home/admin -s /bin/rbash
USER admin
ENV HOME /home/admin

# Expose port 9002 to the outside world
EXPOSE 4000

# Command to run the executable
CMD ["./main"]
