# GuenniGPT

## What is GuenniGPT?

GuenniGPT is a simple discord bot and a fun little side project. It is written in Python and uses the discord.py library.

## What can GuenniGPT do?

GuenniGPTs main function is to greet people that join a voice channel. To do so, it generates a random greeting text with the power of [ChatGPT](openai.com/chatgpt). Using the [Google Text-to-Speech API](https://cloud.google.com/text-to-speech) it then converts the text to speech and plays it in the voice channel.

## How to use GuenniGPT?

### Prepare the environment

Create a folder called `config` and a file `keys.json` inside of it.
You can also create a file called `config.json` in the same folder to configure the bot.

The `config.json` file should look something like this:

```json
{
    "description": "A discord bot that greets people when they join a voice channel.",
    "language": "de",
    "timeout": 600,
    "greeting_styles": {
        "sarcastic": 35,
        "sarcastic and rude": 45,
        "humorous": 20,
        "friendly": 5,
        "old fashioned and formal": 3,
        "dramatic": 4,
        "very serious and formal": 3
    },
    "events": {
        "31.10": [
            "Today is Halloween! Be scray!",
            "Today is Halloween!"
        ],
        "23.12": [
            "Today is Christmas Eve!"
        ]
    }
}
```

You can add more events just by having the date as the key and a list of string as the value. On the specified date, a string from the list will be chosen at random and added to the ChatGPT prompt that generates the greeting text.
The greeeting styles can change the style of the greetings. The key is the string that gets added to the prompt, the value is a "weight" that determines how likely it is that the style is chosen.

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
