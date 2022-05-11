FROM ubuntu:latest

RUN apt update
RUN apt install sudo -y
RUN sudo apt update -y

FROM python:3


WORKDIR /src
COPY client.py client.py
COPY job.py job.py
COPY /filesToDo /filesToDo


RUN pip3 install -r requirements.txt
CMD [ "python", "./client.py" ]