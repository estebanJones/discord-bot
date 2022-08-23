import os
import yt_dlp
import discord
from discord.ext import commands

class YoutubeMusic(commands.Cog):
    song_queue = []

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url):
        self.song_queue.append(url)
        title = await self.get_title_music(url)
        await ctx.send("DJ-Breton rajoute dans sa playlist: {}".format(title))
        channel = self.get_author_channel(ctx)
        self.delete_mp3file_if_exist(ctx)

        if not ctx.guild.voice_client in self.bot.voice_clients:
            print("Connecting channel...")
            await channel.connect()
            
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            self.download_music(url)
            self.rename_mp3files_current_dir("current-song.mp3")
            value = discord.FFmpegPCMAudio("current-song.mp3")
            voice.play(value, after=lambda x=None: self.play_next(voice, ctx, url))
            await ctx.send("DJ-Breton balance: {}".format(title))
            

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            await voice.disconnect()

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await voice.pause()

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await voice.resume()

    async def get_title_music(self, url):
        with yt_dlp.YoutubeDL() as ydl: 
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)

            return video_title
    
    def get_author_channel(self, ctx):
        return ctx.author.voice.channel

    def download_music(self, url):
        os.system("yt-dlp -x --audio-format mp3 {}".format(url))

    def play_next(self, voice, ctx, url):
        self.delete_mp3file_if_exist(ctx)
        self.song_queue.pop(0)
        if len(self.song_queue) >= 1:
            self.download_music(self.song_queue[0])
            self.rename_mp3files_current_dir("current-song.mp3")
            voice.play(discord.FFmpegPCMAudio("current-song.mp3"), after=lambda x=None: self.play_next(voice, ctx, url))

    def rename_mp3files_current_dir(self, name):
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, name)

    def delete_mp3file_if_exist(self, ctx):
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)

async def setup(bot):
    await bot.add_cog(YoutubeMusic(bot))