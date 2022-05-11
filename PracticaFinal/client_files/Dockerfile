FROM ubuntu:latest

RUN apt update
RUN apt-get update
RUN apt install sudo -y
RUN sudo apt update -y
RUN sudo apt install python3-pip -y
RUN apt-get update && apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    unzip \ 
    pkg-config \
    libopencv-dev \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libgtk2.0-dev \ 
    libatlas-base-dev \
    gfortran \
    webp \ 
    zlib1g-dev 

# Install Open CV - Warning, this takes absolutely forever
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/opencv/opencv/archive/3.0.0.zip && \
    unzip 3.0.0.zip && \
    rm 3.0.0.zip && \
    mv opencv-3.0.0 OpenCV && \
    cd OpenCV && \
    mkdir build && \ 
    cd build && \
    cmake \
    -DWITH_QT=ON \ 
    -DWITH_OPENGL=ON \ 
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \ 
    ldconfig


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