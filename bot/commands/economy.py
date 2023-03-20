import sqlite3
import nextcord
from nextcord import PartialInteractionMessage, WebhookMessage
from nextcord.ext import commands


class Konto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="geldbeutel",
        description="Zeigt dir dein Guthaben",
        force_global=True

    )
    async def geld_beutel(
            self,
            ctx: nextcord.Interaction,
            user: nextcord.Member = nextcord.SlashOption(required=False)
    ) -> PartialInteractionMessage | WebhookMessage:

        if user is None:
            # Use own user
            db = sqlite3.connect("ressourcen/bank.db")
            cursor = db.cursor()
            data = cursor.execute(f"SELECT money FROM bank WHERE userId={ctx.user.id}")

            money = data.fetchall()

            if not money:
                return await ctx.send("Du besitzt noch kein Geld.")

            embed_money = nextcord.Embed(
                title="Dein Geld",
                color=nextcord.Color.orange()
            )
            embed_money.set_thumbnail(url=self.bot.user.avatar)
            embed_money.add_field(name="Betrag: ", value=money[0][0])
            return await ctx.send(embed=embed_money)

        db = sqlite3.connect("ressourcen/bank.db")
        cursor = db.cursor()
        data = cursor.execute(f"SELECT money FROM bank WHERE userId={user.id}")

        money = data.fetchall()

        if not money:
            return await ctx.send("Dieser User besitzt noch kein Geld.", ephemeral=True)

        embed_money = nextcord.Embed(
            title="Dein Geld",
            color=nextcord.Color.orange()
        )
        embed_money.add_field(name="Betrag: ", value=money[0][0])
        embed_money.set_thumbnail(url=self.bot.user.avatar)
        await ctx.send(embed=embed_money)


def setup(bot):
    bot.add_cog(Konto(bot))
