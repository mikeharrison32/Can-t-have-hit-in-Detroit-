from discord.ext.commands.bot import Bot, when_mentioned_or
from discord import Intents, app_commands
import config
import discord
from utils import get_channel_name

SERVER_ID = 1256272152727130192

class MainBot(Bot):

    def __init__(self):
        self.config = config
        super().__init__(
            command_prefix='!',
            description=self.config.description,
            intents=Intents.all(),
        )



    async def setup_hook(self):
        await self.load_extensions()
        await self.tree.sync() 

    async def load_extensions(self):
        initial_extensions = [
            'bot.extensions.basic_cog',
            'bot.extensions.casino_game_cog',
            'bot.extensions.moderation_cog',
        ]

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f'Loaded extension: {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')
        

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        await self.tree.sync() 
        

    async def on_member_join(self, member):
        welcome_channel_name = 'welcome'
        channel = discord.utils.get(member.guild.channels, name=welcome_channel_name)

        if channel:
            await channel.send(f'Welcome to da server, {member.mention}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel) or self.user.mentioned_in(message) or (message.reference and message.reference.resolved and message.reference.resolved.author == self.user):
            if message.author.id == 1216358765926809742: 
                guild = self.get_guild(SERVER_ID)
                channel_name = get_channel_name(message.content)
                channel = discord.utils.get(guild.channels, name=channel_name)

                if channel:
                    message_content = f"{message.content[0:message.content.find(get_channel_name(message.content))-1]}"

                    await channel.send(message_content)
                    await message.author.send("Your message has been relayed to the server.")

        await self.process_commands(message)

