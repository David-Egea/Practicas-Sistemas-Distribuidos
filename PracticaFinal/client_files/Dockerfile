FROM ubuntu:latest

RUN apt update
RUN apt install sudo -y
RUN sudo apt update -y

FROM python:3


WORKDIR /src
COPY client.py client.py
COPY configuration.py configuration.py
COPY client_config.ini client_config.ini
COPY requirements.txt requirements.txt
COPY job.py job.py
COPY /filesToDo /filesToDo
RUN mkdir -p /filesDone


RUN pip3 install -r requirements.txt
CMD [ "python", "./client.py" ]