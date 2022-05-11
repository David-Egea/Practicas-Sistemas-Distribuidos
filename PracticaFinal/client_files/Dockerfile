FROM ubuntu:latest

RUN apt update
RUN apt-get update
RUN apt install sudo -y
RUN sudo apt update -y
RUN sudo apt install python3-pip -y
RUN apt-get install ffmpeg libsm6 libxext6  -y


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