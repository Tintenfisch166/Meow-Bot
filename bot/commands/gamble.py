import nextcord
import sqlite3
import random

from nextcord import PartialInteractionMessage, WebhookMessage
from nextcord.ext import commands


class Gamble(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="gamble",
        description="Dein Gambling system.",
        force_global=True,
        default_member_permissions=8
    )
    async def gamble(
            self,
            ctx: nextcord.Interaction,
            dein_einsatz: int
    ) -> PartialInteractionMessage | WebhookMessage:

        db = sqlite3.connect("ressourcen/bank.db")
        cursor = db.cursor()

        data = cursor.execute(f"SELECT money FROM bank WHERE userId={ctx.user.id}")
        money = data.fetchall()

        if not money or money[0][0] < dein_einsatz:
            return await ctx.send("Du besitzt kein Geld oder dein Einsatz ist höher als dein Kontostand.")

        ran_num = random.randint(0, 1)

        if ran_num == 1:
            db.execute(f"UPDATE bank SET money={int(money[0][0]) + int(dein_einsatz)} WHERE userId={ctx.user.id}")
            db.commit()
            db.close()
            return await ctx.send(f"Du hast gewonnen! Dein Kontostand wurde um {dein_einsatz} Euro erhöht.")

        db.execute(f"UPDATE bank SET money={int(money[0][0]) - int(dein_einsatz)} WHERE userId={ctx.user.id}")
        db.commit()
        db.close()
        await ctx.send(f"Du hast verloren! Dein Kontostand wurde um {dein_einsatz} Euro vermindert.")


def setup(bot):
    bot.add_cog(Gamble(bot))
