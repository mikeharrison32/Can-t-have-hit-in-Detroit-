import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os 

load_dotenv()
# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.event
async def on_member_join(member):
    # Specify the channel name where the welcome message should be sent
    welcome_channel_name = 'welcome'
    channel = discord.utils.get(member.guild.channels, name=welcome_channel_name)
    
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')

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



BOT_TOKEN = os.getenv('TOKEN')

# Run the bot
bot.run(BOT_TOKEN)
