# GuenniGPT

## What is GuenniGPT?

GuenniGPT is a simple discord bot and a fun little side project. It is written in Python and uses the discord.py library.

## What can GuenniGPT do?

GuenniGPTs main function is to greet people that join a voice channel. To do so, it generates a random greeting text with the power of [ChatGPT](openai.com/chatgpt). Using the [Google Text-to-Speech API](https://cloud.google.com/text-to-speech) it then converts the text to speech and plays it in the voice channel.

## How to use GuenniGPT?

To use GuenniGPT, you need to have a Google Cloud account and a project with the Text-to-Speech API enabled. You also need to [create a service account and download the credentials as a JSON file](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#before-you-begin). 
You also have to [create a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) and invite it to your server.
The last key you will need is the [OpenAI API key](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

Put the Google TTS key and a `keys.json` file with the other keys in `./files` and you should be good to go.

## How to run GuenniGPT?

You can just clone the repository and run `docker-compose up -d` to run the bot.

If you like the easy way, you can get the image from [GitHub Packages](https://ghcr.io/cheesecaketree/guennigpt:latest) and run it with `docker run -d -v ./config:/usr/src/bot/config ghcr.io/cheesecaketree/guennigpt:latest`.

To run the image you need to mount the `./config` directory to `/usr/src/bot/config`. Then it should work.
