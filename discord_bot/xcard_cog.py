from discord.ext import commands


class XCardHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['x','x-card'])
    async def xcard(self, ctx):
        await ctx.send(f"Someone Posted an Xcard!  Stop it right now!")

    @commands.command(aliases=['o','o-card','awesome'])
    async def ocard(self, ctx):
        await ctx.send(f"This scene is great, keep going!")

    async def cog_after_invoke(self, ctx):
        await ctx.message.delete(delay=0)
