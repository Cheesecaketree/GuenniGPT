# GuenniGPT

## What is GuenniGPT?

GuenniGPT is a discord bot and one of my fun little side projects. It is written in Python and uses AI to generate random greetings for people that join a voice channel. It uses the [ChatGPT](openai.com/chatgpt) model to generate the greeting text and supports multiple Text-to-Speech services to convert the text to speech and play it in the voice channel.

## How to use GuenniGPT?

***Please make sure to read the terms of service and pricing of the respective services the bot uses before using the bot.***

### Prepare the environment

Create a folder called `config` and a file `keys.toml` inside of it.
Put a copy of the config file you from this repository there. You can change the value of the variables there. The file should be self explanatory

### Create the bot and get all the keys

The first step is to create a Discord bot in the [Discord Developer Portal](https://discordpy.readthedocs.io/en/stable/discord.html) and invite it to your server. Add the token to the `keys.toml` file as "discod".

You will also need an OpenAI API key. This is needed for ChatGPT.
A guide on how to get a key can be found [here](https://platform.openai.com/docs/quickstart/account-setup).
Put the key and your organization id in `keys.toml` as "openai" and "openai-org" respectively.

Depending on the Text-to-Speech service you want to use, you will need different keys.
For Google Cloud, you will need a project with the Text-to-Speech API enabled. You can than generate key in json format and add it to the `config` folder.
You can find a guide [here](https://cloud.google.com/text-to-speech/docs/before-you-begin).

If you instead want the more realistic voices from [Elevenlabs](https://elevenlabs.io/), you will to set up an account and subscribe to one of their plans (free tier available). You can find the API key in the profile settings and add it to the `keys.toml` file under the key "elevenlabs".

The `keys.toml` file should look something like this:

```toml

"openai" = "api-key"
"openai-org" = "your-org-id"
"discord" = "discord-bot-token"
"elevenlabs" = "api-key"


```

### Run the bot

You can just clone the repository and run `docker-compose up -d`.

You can also get an image from [GitHub Packages](https://ghcr.io/cheesecaketree/guennigpt:latest) and run it with `docker run -d -v ./config:/usr/src/bot/config ghcr.io/cheesecaketree/guennigpt:latest`.
Run this command in the directory where the `config` folder is located, so it gets mounted into the container or change the directory accordingly.


