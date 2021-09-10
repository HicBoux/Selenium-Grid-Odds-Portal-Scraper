FROM python:3.7

ENV PYTHONBUFFERED 1
COPY ./requirements.txt /requirements.txt

# Set the locale in container
ENV LC_ALL en_US.UTF-8 
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en     
ENV LC_TIME en_BW.UTF-8

RUN pip3 install -U pip setuptools
RUN pip3 install -U -r /requirements.txt

RUN mkdir /scraper
COPY ./scraper /scraper
WORKDIR /scraper
