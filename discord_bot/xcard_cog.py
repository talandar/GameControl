from discord.ext import commands
import discord
from utils import try_delete


class XCardHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['x','x-card'])
    async def xcard(self, ctx):
        """Call for an X card, to stop the current action in case the current action is uncomfortable."""
        await ctx.send("X-Card - Let's change things up...")
        await ctx.send(file=discord.File('./images/xcard.png'))

    @commands.command(aliases=['o','o-card','awesome'])
    async def ocard(self, ctx):
        """Call for the O card - indicating that what is going on is super cool."""
        await ctx.send("This scene is great, keep going! :sunglasses:")

    @commands.command(aliases=['fade','fadetoblack'])
    async def fadecard(self, ctx):
        """Call for a fade to black.  This scene can happen, but lets do that offscreen."""
        await ctx.send("Fade-Card Called.  Lets fade this scene to black...")

    async def cog_after_invoke(self, ctx):
        await try_delete(ctx.message)
