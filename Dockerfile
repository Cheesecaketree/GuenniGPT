FROM gorialis/discord.py:3.11.2-bullseye-master-full

WORKDIR /usr/src/bot

RUN apt update

RUN apt install libffi-dev libnacl-dev python3-dev -y


# install python libraries
COPY requirements.txt .

RUN pip install -r requirements.txt

# copy source code
COPY app .
COPY config ./config



ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD [ "python3", "-u", "discord_bot.py" ]