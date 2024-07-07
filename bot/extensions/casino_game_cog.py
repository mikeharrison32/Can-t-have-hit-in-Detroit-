from discord.ext import commands
from discord import app_commands
import random
import discord
from discord.ext.commands import Context
class CasinoGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wallets = {}

    @commands.command(name='balance', description='Check your balance')
    async def check_balance(self, ctx: Context):
        member = ctx.author
        if member.id not in self.wallets:
            self.wallets[member.id] = 100
        balance = self.wallets[member.id]
        await ctx.send(f'Your current balance is {balance} coins.')

    @commands.command(name='cf', description='Flip a coin with the specified number of coins')
    async def coin_flip(self, ctx: Context, amount: int):
        member = ctx.author
        if member.id not in self.wallets:
            self.wallets[member.id] = 100

        if amount <= 0 or amount > self.wallets[member.id]:
            await ctx.send('Invalid amount. get more by begging mike!!')
            return

        result = random.choice(['heads', 'tails'])
        if result == 'heads':
            self.wallets[member.id] += amount
            await ctx.send(f'You won! Your new balance is {self.wallets[member.id]} coins.')
        else:
            self.wallets[member.id] -= amount
            await ctx.send(f'You lost! Your new balance is {self.wallets[member.id]} coins.')

    @commands.command(name='rob', help='Attempt to rob coins from another member')
    async def rob(self, ctx, target: discord.Member):
        member = ctx.author
        if member.id not in self.wallets:
            self.wallets[member.id] = 100

        if target.id not in self.wallets:
            self.wallets[target.id] = 100

        if member == target:
            await ctx.send("You can't rob yourself!")
            return

        success_rate = random.randint(1, 100)
        if success_rate <= 50:

            robbed_amount = random.randint(1, self.wallets[target.id])
            self.wallets[target.id] -= robbed_amount
            self.wallets[member.id] += robbed_amount
            await ctx.send(f"You successfully robbed {robbed_amount} coins from {target.display_name}! Your new balance is {self.wallets[member.id]} coins.")
        else:

            await ctx.send(f"Attempt to rob {target.display_name} failed! You lost 20 coins as penalty.")


            self.wallets[member.id] -= 20

async def setup(bot):
    await bot.add_cog(CasinoGame(bot))
