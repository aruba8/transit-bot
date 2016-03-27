FROM python:3.5
MAINTAINER Erik Khalimov <biomaks@gmail.com>
RUN apt-get update && apt-get install -y curl vim nano
WORKDIR /application
ADD application /application
RUN pip install -r requirements.txt
CMD python run.py