import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os 
from discord import app_commands

load_dotenv()
# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

SERVER_ID = 1256272152727130192
bot = commands.Bot(command_prefix='!', intents=intents)


tree = bot.tree

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await tree.sync()


@bot.event
async def on_member_join(member):
    # Specify the channel name where the welcome message should be sent
    welcome_channel_name = 'welcome'
    channel = discord.utils.get(member.guild.channels, name=welcome_channel_name)
    
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')


# Slash Command: /ping
@tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

def get_after_backslash(text):
    index = text.find('?')  # Find the index of the first backslash
    if index != -1:
        return text[index+1:]  # Return the substring after the backslash
    else:
        return None 


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    

    # Check if the message is a DM or mentions the bot or is a reply to the bot
    if isinstance(message.channel, discord.DMChannel) or bot.user.mentioned_in(message) or (message.reference and message.reference.resolved and message.reference.resolved.author == bot.user):
        # Check if the message author is you (replace with your user ID)
        if message.author.id == 1216358765926809742: 
 

            guild = bot.get_guild(SERVER_ID)
            channel_name = get_after_backslash(message.content)
            channel = discord.utils.get(guild.channels, name=channel_name)

            if channel:
                # Construct the message content
                message_content = f"{message.content[0:message.content.find(get_after_backslash(message.content))-1]}"

                # Send the message to the specified channel
                await channel.send(message_content)

                # Optionally, reply back to the user in DMs acknowledging receipt
                await message.author.send("Your message has been relayed to the server.")

    # Allow commands to be processed
    await bot.process_commands(message)


# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Command: Echo
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

# Command: Clear
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)  # +1 to remove the command message as well

# Command: Kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention} for {reason}')

# Command: Ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} for {reason}')

# Command: Unban
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# Command: Mute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mute_role = discord.utils.get(guild.roles, name="Muted")

    if not mute_role:
        mute_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'Muted {member.mention} for {reason}')

# Command: Unmute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mute_role)
    await ctx.send(f'Unmuted {member.mention}')

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    # If no member is specified, use the command invoker
    member = member or ctx.author
    
    # Create an embed message with the user's information
    embed = discord.Embed(title=f"{member.name}'s Info", description=f"Here is {member.mention}'s info", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="Top Role", value=member.top_role, inline=True)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    
    # Send the embed message to the channel
    await ctx.send(embed=embed)


wallets = {}

# Command: Check Balance
@bot.command(name='balance', help='Check your balance')
async def check_balance(ctx):
    member = ctx.author
    if member.id not in wallets:
        wallets[member.id] = 100  # Initial balance of 100 coins
    balance = wallets[member.id]
    await ctx.send(f'Your current balance is {balance} coins.')

# Command: Coin Flip
@bot.command(name='cf', help='Flip a coin with the specified number of coins')
async def coin_flip(ctx, amount: int):
    member = ctx.author
    if member.id not in wallets:
        wallets[member.id] = 100  # Initial balance of 100 coins

    if amount <= 0:
        await ctx.send('Please enter a valid amount of coins to flip.')
        return

    if amount > wallets[member.id]:
        await ctx.send('You do not have enough coins.')
        return

    # Perform the coin flip
    result = random.choice(['heads', 'tails'])
    if result == 'heads':
        wallets[member.id] += amount
        await ctx.send(f'You won! Your new balance is {wallets[member.id]} coins.')
    else:
        wallets[member.id] -= amount
        await ctx.send(f'You lost! Your new balance is {wallets[member.id]} coins.')


# Command: Rob
@bot.command(name='rob', help='Attempt to rob coins from another member')
async def rob(ctx, target: discord.Member):
    member = ctx.author
    if member.id not in wallets:
        wallets[member.id] = 100  # Initial balance of 100 coins

    if target.id not in wallets:
        wallets[target.id] = 100  # Initial balance of 100 coins

    if member == target:
        await ctx.send("You can't rob yourself!")
        return

    # Determine the success rate of the robbery
    success_rate = random.randint(1, 100)
    if success_rate <= 50:  # Adjust success rate as desired
        # Successful robbery
        robbed_amount = random.randint(1, wallets[target.id])
        wallets[target.id] -= robbed_amount
        wallets[member.id] += robbed_amount
        await ctx.send(f"You successfully robbed {robbed_amount} coins from {target.display_name}! Your new balance is {wallets[member.id]} coins.")
    else:
        # Unsuccessful robbery
        await ctx.send(f"Attempt to rob {target.display_name} failed! You lost 20 coins as penalty.")

        # Penalty for unsuccessful robbery
        wallets[member.id] -= 20

BOT_TOKEN = os.getenv('TOKEN')

# Run the bot
bot.run(BOT_TOKEN)
