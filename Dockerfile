FROM python:3.6

RUN pip install --upgrade pip

WORKDIR /waimea
COPY ./ /waimea
RUN pip install -e /waimea

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-add-repository -y 'deb http://security.debian.org/debian-security stretch/updates main'
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk curl