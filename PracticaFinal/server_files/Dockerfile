FROM ubuntu:latest

RUN apt update
RUN apt-get update
RUN apt install sudo -y
RUN sudo apt update -y
RUN sudo apt install python3-pip -y

FROM python:3

WORKDIR /src
COPY master_node.py master_node.py
COPY server.py server.py
COPY configuration.py configuration.py
COPY service_server.py service_server.py
COPY server_config.ini server_config.ini
COPY requirements.txt requirements.txt
COPY job.py job.py

RUN mkdir -p /src/TaskInbox
RUN mkdir -p /src/ResponseOutBox


RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python-headless
CMD [ "python", "./server.py" ]