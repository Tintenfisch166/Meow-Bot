import nextcord
import asyncio
from nextcord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(seconds=30)
    async def status(self):
        await self.bot.change_presence(
            activity=nextcord.Game("Splatoon mit Tudor"),
            status=nextcord.Status.do_not_disturb
        )
        await asyncio.sleep(15)
        await self.bot.change_presence(
            activity=nextcord.Game("Splatoon mit Dilshaan"),
            status=nextcord.Status.do_not_disturb
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(Status(bot))
