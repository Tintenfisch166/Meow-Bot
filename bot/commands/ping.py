import nextcord
from nextcord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="ping",
        description="Zeigt den Ping des Bots an.",
        force_global=True
    )
    async def ping(self, ctx: nextcord.Interaction):
        await ctx.send(f"Der Ping liegt bei: {round(self.bot.latency * 100)}ms")


def setup(bot):
    bot.add_cog(Ping(bot))
