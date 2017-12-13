FROM ubuntu

RUN \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y python python-dev python-pip python-virtualenv

RUN pip install numpy
RUN pip install requests

COPY . /algorithm/

WORKDIR /algorithm/

RUN ls