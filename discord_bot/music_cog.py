import asyncio
import json
from typing import AsyncIterable
import discord
from discord.ext import commands
import youtube_dl


import playlist

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': './audio/%(title)s-%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_playlists = {}
        self._now_playing = None

    @commands.command()
    async def join(self, ctx):
        """Joins your current voice channel"""
        channel = None
        if ctx.author.voice:
            channel = ctx.author.voice.channel
        if channel:
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)
            await channel.connect()
        else:
            await ctx.send("You're not in a voice channel!  I don't know what channel to join! :confounded:")
    

    @commands.command()
    async def stream(self, ctx, *, url):
        """(url): Immediately streams from a url, does not modify playlists."""
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        self._now_playing = f"Now streaming {player.title}"
        await ctx.send(self._now_playing)

    @commands.command()
    async def volume(self, ctx, volume: int):
        """(volume [0-100]): Changes the player's volume"""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        volume = max(0, min(volume, 100))
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def leave(self, ctx):
        """Stops and disconnects the bot from voice"""
        self._now_playing = None
        await ctx.voice_client.disconnect()

    @commands.command()
    async def stop(self, ctx):
        """Stops playing the current playlist or stream without leaving the channel"""
        self._now_playing = None
        data = self._get_data(ctx)
        data.stop()
        ctx.voice_client.stop()

    @commands.command(aliases=['playlists'])
    async def listplaylists(self, ctx):
        """list the existing playlists"""
        data = self._get_data(ctx)
        lists = data.list_playlists()
        output = "Here's the playlists that I currently have:\n"
        if lists:
            print(lists)
            lists = "\n".join(lists)
            output = output + lists
        await ctx.send(output)

    @commands.command()
    async def createplaylist(self, ctx, name:str):
        """(name): create a new playlist by name"""
        data = self._get_data(ctx)
        success = data.add_playlist(name)
        if success:
            await ctx.send(f"Created new playlist with name \"{name}\"")
        else:
            await ctx.send(f"Couldn't create playlist with name \"{name}\".  Sorry :sob:")

    @commands.command()
    async def deleteplaylist(self, ctx, name:str):
        """(name): Delete an existing playlist by name"""
        data = self._get_data(ctx)
        if data.current_playlist() == name:
            #this should finish the current song then stop playing.
            data.stop()
        success = data.remove_playlist(name)
        if success:
            await ctx.send(f"Removed the playlist called \"{name}\"")
        else:
            await ctx.send(f"Something went wrong removing the playlist called \"{name}\".  Sorry :sob:")

    @commands.command()
    async def songs(self, ctx, name:str):
        """(playlist name): Get the list of songs in a playlist"""
        data = self._get_data(ctx)
        songs = data.songs_in_list(name)
        songs = '\n'.join(songs)
        output = f"Here's what's in {name}:\n{songs}"
        await ctx.send(output)

    @commands.command()
    async def addsong(self, ctx, playlist_name:str, song_url:str):
        """(playlist) (song url): add a song to a playlist"""
        data = self._get_data(ctx)
        if data.add_to_playlist(playlist_name,song_url):
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
        else:
            await ctx.send("Something went wrong, sorry!  Does the playlist exist?")

    @commands.command()
    async def removesong(self, ctx, playlist_name:str, song_url:str):
        """(playlist) (song url): remove a song from a playlist"""
        data = self._get_data(ctx)
        if data.remove_from_playlist(playlist_name,song_url):
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
        else:
            await ctx.send("Something went wrong, sorry!  Does the playlist exist?")

    @commands.command()
    async def play(self, ctx, playlist_name:str):
        """(playlist): Play a playlist.  Loops randomly through songs in the list."""
        print("in play")
        data = self._get_data(ctx)
        song = data.play(playlist_name)
        if song: 
            player = await YTDLSource.from_url(song, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else self._song_over_callback(ctx))
            self._now_playing = f"Now playing {player.title} in playlist {data.current_playlist()}"
            await ctx.send(self._now_playing)
        else:
            self._now_playing = None
            await ctx.send("No more songs to play.  Did the playlist get deleted?")

    def _song_over_callback(self, ctx):
        print('song over callback')
        pl = self._get_data(ctx).current_playlist()
        if pl:
            asyncio.run_coroutine_threadsafe(self.play(ctx, pl), loop=self.bot.loop)

    @commands.command(aliases=["currentsong"])
    async def nowplaying(self, ctx):
        """get the currently playing song and playlist"""
        if self._now_playing:
            await ctx.send(self._now_playing)
        else:
            await ctx.send("Not currently playing!")

    @commands.command(aliases=["skip"])
    async def next(self, ctx):
        """Go to the next song in the playlist.  If streaming, ends the song."""
        print('in next')
        #TODO next very likely to dupe-play, because the stop calls next, 
        #then this calls next, and they both end up going to a new song, losing the current state
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    def _get_data(self, context):
        id = context.guild.id
        if id in self.server_playlists:
            return self.server_playlists[id]
        else:
            data = playlist.ServerPlaylist(id)
            self.server_playlists[id] = data
            return data

    #Disable this - it was for playing downloaded files
    #@commands.command()
    async def play_downloaded(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    #Disable this - it downloads the file
    #@commands.command()
    async def download(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()