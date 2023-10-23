# GuenniGPT

## What is GuenniGPT?

GuenniGPT is a simple discord bot and a fun little side project. It is written in Python and uses the discord.py library.

## What can GuenniGPT do?

GuenniGPTs main function is to greet people that join a voice channel. To do so, it generates a random greeting text with the power of [ChatGPT](openai.com/chatgpt). Using the [Google Text-to-Speech API](https://cloud.google.com/text-to-speech) it then converts the text to speech and plays it in the voice channel.

## How to use GuenniGPT?

### Prepare the environment

Create a folder called `config` and a file `keys.json` inside of it.
You can also create a file called `config.json` in the same folder to configure the bot. If you want to use the events feature, you also need to create a file called `events.json` in the same folder. Events are special texts that are added to the ChatGPT prompts on specific dates.

The `config.json` file should look like this:

```json
{
    
}
```

The `events.json` file should look like this:

```json
{
    "24.12": ["Today is Christmas Eve!"],

}
```

### Create the bot and get all the keys

The first step is to create a Discord bot in the [Discord Developer Portal](https://discordpy.readthedocs.io/en/stable/discord.html) and invite it to your server. Add the token to the `keys.json` file.

For the Text-to-Speech features you need a Google Cloud account and a project with the Text-to-Speech API enabled.
You also need to [create a service account and download the credentials as a JSON file](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#before-you-begin). The json file goes into the `config` folder.

The last key you will need is the [OpenAI API key](https://beta.openai.com/docs/developer-quickstart/your-api-keys). Put the key and your organization id in `keys.json`.

The `keys.json` file should look something like this:

```json
{
    "openai": "api-key",
    "openai-org": "your-org-id",
    "discord": "discord-bot-token",
}

```

## How to run GuenniGPT?

You can just clone the repository and run `docker-compose up -d`.

You can also get an image at [GitHub Packages](https://ghcr.io/cheesecaketree/guennigpt:latest) and run it with `docker run -d -v ./config:/usr/src/bot/config ghcr.io/cheesecaketree/guennigpt:latest`.
Mounting the `./config` directory to `/usr/src/bot/config` is necessary to provide the keys to the bot.
