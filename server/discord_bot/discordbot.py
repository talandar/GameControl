import os

import discord
from dotenv import load_dotenv
from battle_cog import BattleTracker


class TobyTrack(discord.ext.commands.Bot):

    prefix_map = {}
    default_prefix = '+'

    def __init__(self):
        super().__init__(command_prefix=self.get_server_prefix)
        self.add_cog(BattleTracker(self))
        self.setup_prefix_map()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    def get_server_prefix(self, bot, message):
        server = message.guild.id
        return self.prefix_map.get(server, self.default_prefix)

    def setup_prefix_map(self):
        @self.command(name="prefix", pass_context=True)
        async def set_server_prefix(ctx, prefix: str):
            self.prefix_map[ctx.guild.id] = prefix
            print(f"Set prefix for bot to {prefix} for server {ctx.guild} ({ctx.guild.id})")
            await ctx.send(f"Toby will now listen for prefix '{prefix}' on this server.")


def main():
    """run the toby tracker.  This Method blocks"""
    load_dotenv()
    client = TobyTrack()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)


if __name__ == "__main__":
    main()
