FROM ubuntu:latest

RUN apt update
RUN apt-get update
RUN apt install sudo -y
RUN sudo apt update -y
RUN sudo apt install python3-pip -y




FROM python:3


WORKDIR /src
COPY client.py client.py
COPY configuration.py configuration.py
COPY client_config.ini client_config.ini
COPY requirements.txt requirements.txt
COPY job.py job.py
RUN mkdir -p /filesToDo
COPY /filesToDo/ /filesToDo/
RUN mkdir -p /filesDone


RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python-headless
CMD [ "python3", "./client.py" ]