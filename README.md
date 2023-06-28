# BrittaBot: a shitty Community script-generator chatbot for Discord

## TODOS

- Investigate how to dynamically change discord bot nickname and avatar per character
- Generate python instances per character, tied to specific prompt
- Look into GPT functions to feed to themselves
- Come up with a good macroprompt

## What is this?

A Discord that [TODO] using LLM and diffusion AI technologies.

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

Learn more in the [blog post](https://recordcrash.substack.com).

## Credits

- Dan Harmon and the Community S1, S2, S3, S5 and S6 writing teams and actors for the inspiration.
- [AUTOMATIC1111](https://github.com/AUTOMATIC1111) for his amazing Stable Diffusion UI.
- [OpenAI](https://openai.com/) and their LLM team.