﻿# BrittaBot: a Community script-generator chatbot for Discord

VERY in progress, but this might never be finished so I'm uploading it anyway.

## TODOS

- Look into better or finetuned models—GPT-4 is really good but incredibly expensive and makes scenes too short, while GPT-3 can barely figure out the correct functions to call. 
- Investigate how to dynamically change discord bot nickname and avatar per character
- Generate python instances per character, tied to specific prompt?
- Come up with a better macroprompt
- Generate images??

## What is this?

A Discord that generates Community scripts using LLM and diffusion AI technologies. DOESN'T REALLY WORK YET.

## How to use

1. Create a virtual environment and install the requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create a Discord bot and get its token. See [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) for more information.
3. Create a `.env` file from `.env.example` and fill in the Discord and OpenAI tokens.
4. If you want image generation, download AUTOMATIC1111's Stable Diffusion UI and keep it up at the default port. If you don't want image generation, you might need to lightly edit the code in `alchemy_bot.py`.
5. Run the bot:

```bash
python3 bot.py
```

6. Invite the bot to your server and launch it with [...]

7. Alternatively, run test.py to manually generate scripts locally.

Learn more in the [blog post](https://recordcrash.substack.com) that does not exist yet.

## Credits

- Dan Harmon and the Community S1, S2, S3, S5 and S6 writing teams and actors for the inspiration.
- [OpenAI](https://openai.com/) and their LLM team.
