import os
from click import pass_context

import discord
from xcard_cog import XCardHandler
from music_cog import Music
from dice_cog import Dice
from dotenv import load_dotenv
from battle_cog import BattleTracker
from utils import *


class TobyTrack(discord.ext.commands.Bot):

    prefix_map = {}
    default_prefix = '+'

    def __init__(self):
        super().__init__(command_prefix=self.get_server_prefix)
        self.add_cog(Music(self))
        self.add_cog(XCardHandler(self))
        self.add_cog(Dice(self))
        self.setup_prefix_map()
        self.add_general_commands()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print(f'running code built on {get_version()}')

    def get_server_prefix(self, bot, message):
        server = message.guild.id
        return self.prefix_map.get(server, self.default_prefix)

    def setup_prefix_map(self):
        @self.command(name="prefix", pass_context=True, help="Set the prefix for triggering Toby to listen to commands.")
        async def set_server_prefix(ctx, prefix: str):
            self.prefix_map[ctx.guild.id] = prefix
            print(f"Set prefix for bot to {prefix} for server {ctx.guild} ({ctx.guild.id})")
            await ctx.send(f"Toby will now listen for prefix '{prefix}' on this server.")

    def add_general_commands(self):
        @self.command(name="cleanup", pass_context=True, help="Clean up commands sent by Toby, as well as any commands sent by players to Toby")
        async def cleanup_messages(ctx):
            async for message in ctx.channel.history(limit=200):
                if message.author == ctx.bot.user:
                    try:
                        await message.delete()
                    except Exception:
                        pass
        @self.command(name="version", pass_context=True, help="Get Toby's build version.")
        async def version(ctx):
            await ctx.send(f"Version: {get_version()}")

def main():
    """run the toby tracker.  This Method blocks"""
    load_dotenv()
    client = TobyTrack()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)


if __name__ == "__main__":
    main()
