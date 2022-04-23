FROM ubuntu:latest

RUN apt update
RUN apt install sudo -y
RUN sudo apt update -y

FROM python:3



COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "python", "./my_script.py" ]