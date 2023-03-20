import sqlite3
import nextcord
from nextcord import PartialInteractionMessage, WebhookMessage
from nextcord.ext import commands


class RemoveMoney(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="geld-löschen",
        description="Ziehe einen Spieler Geld aus der Tasche.",
        force_global=True,
        default_member_permissions=8
    )
    async def add_money(
            self,
            ctx: nextcord.Interaction,
            user: nextcord.Member,
            geldbetrag: int
    ) -> PartialInteractionMessage | WebhookMessage:

        db = sqlite3.connect("ressourcen/bank.db")
        cursor = db.cursor()

        data = cursor.execute(f"SELECT money FROM bank WHERE userId={user.id}")
        money = data.fetchall()

        if not money:
            return await ctx.send(f"Der user {user.name} besitzt kein Geld.", ephemeral=True)

        if money[0][0] < geldbetrag:
            return await ctx.send("Du kannst nicht mehr Geld abziehen, als der User besitzt", ephemeral=True)

        db.execute(f"UPDATE bank SET money={int(money[0][0] - geldbetrag)} WHERE userId={user.id}")
        db.commit()
        db.close()
        await ctx.send(f"Du hast {geldbetrag} Euro den user {user.name} gegeben.", ephemeral=True)


def setup(bot):
    bot.add_cog(RemoveMoney(bot))
