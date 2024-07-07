from discord.ext.commands.cog import Cog
from discord.ext.commands import hybrid_group, Context
from discord import app_commands
import discord


class BasicCog(Cog):
    def __init__(self, bot):
        self.bot = bot 


    @app_commands.command(name="ping", description="Replies with Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Fuck you!')

    @app_commands.command(name="echo", description="Repeats your message")
    async def echo(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)


async def setup(bot):
    await bot.add_cog(BasicCog(bot))


