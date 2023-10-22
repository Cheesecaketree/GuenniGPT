FROM python:3.11.4-buster
FROM gorialis/discord.py:3.11.2-bullseye-master-full

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .


RUN apt update

RUN apt install libffi-dev libnacl-dev python3-dev -y


# install python libraries
#COPY requirements.txt .
RUN pip install -r requirements.txt

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# RUN echo "Europe/Berlin" > /etc/timezone && \ dpkg-reconfigure -f noninteractive tzdata



CMD [ "python3", "discord_bot.py" ]