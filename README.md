# GuenniGPT

## What is GuenniGPT?

GuenniGPT is a simple discord bot and a fun little side project of mine. It is written in Python and uses the discord.py library.

## What can GuenniGPT do?

GuenniGPTs main function is to greet people that join a voice channel. To do so, it generates a random greeting text with the power of [ChatGPT](openai.com/chatgpt). Using the [Google Text-to-Speech API](https://cloud.google.com/text-to-speech) it then converts the text to speech and plays it in the voice channel.

## How to use GuenniGPT?

To use GuenniGPT, you need to have a Google Cloud account and a project with the Text-to-Speech API enabled. You also need to [create a service account and download the credentials as a JSON file](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#before-you-begin). 
You also have to [create a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) and invite it to your server.
The last key you will need is the [OpenAI API key](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

Put all of these keys into a file `./files/keys.json` and you should be good to go.

## How to run GuenniGPT?

Just run the docker compose file.
There is also an docker image available but you have to figure out how to get the keys into the container yourself.
Maybe if I start understanding what I am doing I will make it easier to use in the future.
