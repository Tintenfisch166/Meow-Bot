import sqlite3
import nextcord
from nextcord import PartialInteractionMessage, WebhookMessage
from nextcord.ext import commands


class AddMoney(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="geld-hinzufügen",
        description="Gebe einen Spieler Geld",
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
            db.execute(f"INSERT INTO bank (userId, money) VALUES ({int(user.id)}, {int(geldbetrag)})")
            db.commit()
            db.close()
            return await ctx.send(f"Du hast den user {geldbetrag} Euro hinzugefügt.", ephemeral=True)

        db.execute(f"UPDATE bank SET money={int(money[0][0] + geldbetrag)} WHERE userId={user.id}")
        db.commit()
        db.close()
        await ctx.send(f"Du hast {geldbetrag} Euro den user {user.name} gegeben.", ephemeral=True)


def setup(bot):
    bot.add_cog(AddMoney(bot))
