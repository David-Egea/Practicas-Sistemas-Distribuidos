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
RUN mkdir -p /src/files/filesToDo
COPY /files/filesToDo/cat_0018.jpg /src/files/filesToDo/cat_0018.jpg
COPY /files/filesToDo/cat_0019.jpg /src/files/filesToDo/cat_0019.jpg
COPY /files/filesToDo/cat_0020.jpg /src/files/filesToDo/cat_0020.jpg
RUN mkdir -p /src/files/filesDone


RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python-headless
CMD [ "python", "./client.py" ]