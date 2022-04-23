FROM ubuntu:latest

RUN apt update
RUN apt install sudo -y
RUN sudo apt update -y

WORKDIR /tmp

RUN sudo apt install curl build-essential -y
RUN ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime
RUN sudo apt-get -y install tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN sudo apt install tcl -yq
RUN curl -O http://download.redis.io/releases/redis-5.0.7.tar.gz
RUN tar xzvf redis-5.0.7.tar.gz

WORKDIR /tmp/redis-5.0.7

RUN make
RUN make test
RUN sudo make install

RUN sudo mkdir /etc/redis /var/log/redis /var/lib/redis
RUN sudo cp /tmp/redis-5.0.7/redis.conf /etc/redis
RUN sudo cp /etc/redis/redis.conf /etc/redis/redis.slv.conf

ADD code/my-redis.conf .

RUN cat my-redis.conf >> /etc/redis/redis.conf
RUN sed "s/redis-server.log/redis-server.slv.log/g" my-redis.conf >> /etc/redis/redis.slv.conf

CMD sed -i "s/<ip_address_docker>/$(hostname -i)/g" /etc/redis/redis.conf && \
  sed -i "s/<ip_address_docker>/$(hostname -i)/g" /etc/redis/redis.slv.conf && \
  sed -i "s/<REDIS_PORT>/$MASTER_PORT/g" /etc/redis/redis.conf && \
  sed -i "s/<REDIS_PORT>/$SLAVE_PORT/g" /etc/redis/redis.slv.conf && \
  sudo redis-server /etc/redis/redis.conf && \
  sudo redis-server /etc/redis/redis.slv.conf && \
  echo 'Docker IP address: \033[46m'$(hostname -i)'\033[0m' && \
  bash
