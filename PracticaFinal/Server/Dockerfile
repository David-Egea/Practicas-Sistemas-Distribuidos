FROM ubuntu:latest

RUN apt update
RUN apt install sudo -y
RUN sudo apt update -y

FROM python:3



COPY requirements.txt requirements.txt
COPY ServerNode.py ServerNode.py 
RUN pip3 install -r requirements.txt
RUN mkdir -p /filesToDo
RUN mkdir -p /filesDone
CMD [ "python", "./ServerNode.py" ]