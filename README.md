# GuenniGPT

## What is GuenniGPT?

GuenniGPT is a discord bot and one of my fun little side projects. It is written in Python and uses AI to generate random greetings for people that join a voice channel. It uses the [ChatGPT](openai.com/chatgpt) model to generate the greeting text and supports multiple Text-to-Speech services to convert the text to speech and play it in the voice channel.

## General information

### Currently supported Text-to-Speech services

- OpenAI TTS
- Elevenlabs TTS

### Currently supported LLMs / APIs for text generation

- OpenAI ChatGPT with all models
- Groq with all models


## How to use GuenniGPT?

***Please make sure to read the terms of service and pricing of the respective services the bot uses before using the bot.***

### Prepare the environment

Create a folder called `config` and a file `keys.toml` inside of it.
Put a copy of the config file you from this repository there. You can change the value of the variables there. The file should be self explanatory
Make sure to adapt the services for text generation and Text-to-Speech to your needs!

### Create the bot and get all the keys

The first step is to create a Discord bot in the [Discord Developer Portal](https://discordpy.readthedocs.io/en/stable/discord.html) and invite it to your server. Add the token to the `keys.toml` file as "discod".

Depending on what services you choose for Text-to-Speech and text generation, you will need different keys.
A guide on how to aquire OpenAI API keys

If you want to use OpenAI for either text generation or Text-to-Speech, you will need to create an account and get an API key. You can find the key in the profile settings and add it to the `keys.toml` file under the key "openai".

For Elevenlabs, you will need to create an account and subscribe to one of their plans. You can find the API key in the profile settings and add it to the `keys.toml` file under the key "elevenlabs". The free tier only offers a limited amount of characters per month. Currently automatic switching between two services is not implemented so keep the limit in mind. The feature is planned and would allow to use the free tier of Elevenlabs and switch to OpenAI if the limit is reached.

If you want to use Groq for text generation, you will need to create an account and get an API key. You can find the key in the profile settings and add it to the `keys.toml` file under the key "groq".

Looking at the current pricing of the services, I would recommend using OpenAI for Text-to-Speech and groq for text generation. With groq you also get a good selection of models to choose from.

The `keys.toml` file should look something like this:

```toml

"openai" = "api-key"
"discord" = "discord-bot-token"
"elevenlabs" = "api-key"
"groq" = "api-key"


```

### Run the bot

You can just clone the repository and run `docker-compose up -d`.

You can also get an image from [GitHub Packages](https://ghcr.io/cheesecaketree/guennigpt:latest) and run it with `docker run -d -v ./config:/usr/src/bot/config ghcr.io/cheesecaketree/guennigpt:latest`.
Run this command in the directory where the `config` folder is located, so it gets mounted into the container or change the directory accordingly.


