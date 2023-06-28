import asyncio

import discord
from discord import app_commands
from discord.ext import commands


class GenerateLine(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def get_character(self, message: str):
        return message.split(" ")[0]

    @app_commands.command(name="generateline", description="For now, just a test command with one string argument")
    async def generateline(self, interaction: discord.Interaction, user_input: str):
        # Send auto-destruct message
        msg = await interaction.response.send_message(f"Starting dummy task with input: {user_input}", ephemeral=True)

        # Dummy task
        print("Starting task")
        await asyncio.create_task(print(msg))

        # Send real message when task is resolved
        followup = await interaction.followup.send(f"Test2 with {user_input}")


async def setup(bot: commands.Bot):
    await bot.add_cog(GenerateLine(bot))
    print("Loaded generate_line cog successfully")
