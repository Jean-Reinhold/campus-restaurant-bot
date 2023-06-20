FROM python:3.10-slim-buster

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install requests temporal-cache pytz    
RUN pip3 install python-telegram-bot --pre

COPY . .

ENV TOKEN="PLACE YOUR TOKEN HERE"

CMD [ "python3", "main.py"]
