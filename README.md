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

Just run the docker compose file.
There is also a docker image available but you have to figure out how it works. I somehow got it to work but I dont really understand what I did. If I manage to understand this stuff, I will add an instruction here
