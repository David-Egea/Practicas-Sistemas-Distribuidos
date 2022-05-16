FROM ubuntu:latest

RUN apt update
RUN apt install sudo -y
RUN sudo apt update -y

FROM python:3


WORKDIR /src

COPY slave.py slave.py
COPY configuration.py configuration.py
COPY slave_config.ini slave_config.ini
COPY requirements.txt requirements.txt
COPY job.py job.py

RUN mkdir -p /src/task_modules

COPY /task_modules/image_task_module.py /src/task_modules/image_task_module.py
COPY /task_modules/task_module.py /src/task_modules/task_module.py
COPY /task_modules/yolov5_task_module.py /src/task_modules/yolov5_task_module.py


RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python-headless
CMD [ "python", "./slave_node.py" ]