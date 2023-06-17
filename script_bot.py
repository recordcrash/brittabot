import asyncio
import os

import discord
from cogwatch import watch
from discord.ext import commands
from dotenv import load_dotenv


class ScriptBot(commands.Bot):
    load_dotenv()
    discord_token = os.getenv("DISCORD_TOKEN")
    owner_id = os.getenv("ADMIN_IDS")
    owner = discord.Object(id=owner_id)
    guild_id = 152981670507577344
    guild = discord.Object(id=guild_id)
    channel_id = 1116406964533084300
    channel = discord.Object(id=channel_id)
    intents = discord.Intents.default()
    intents.message_content = True  # v2
    extensions = [
        "commands.generate_line",
    ]

    def __init__(self):
        super().__init__(command_prefix='D-->', owner_id=self.owner_id, intents=self.intents)

    async def sync_commands(self):
        self.tree.copy_global_to(guild=self.guild)
        all_commands = await self.tree.sync(guild=self.guild)
        print(f"Synced {len(all_commands)} commands to the guild")

    @watch(path="commands", preload=True)
    async def on_ready(self):
        print(f"Logged in as {self.user.name} ({self.user.id})")
        for extension in self.extensions:
            await self.load_extension(extension)
        # load the slash command associated with generate_line
        # sync_commands()


async def main():
    client = ScriptBot()
    await client.start(client.discord_token)


if __name__ == "__main__":
    asyncio.run(main())
