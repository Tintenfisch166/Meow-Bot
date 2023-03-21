import nextcord
import os
from nextcord.ext import commands
from src.loader.jsonLoader import Token


class MeowBot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=nextcord.Intents.all()
        )

        self.token = Token().get_token()

        # load requirements
        self.remove_command("help")
        print("Requirements loaded")

        for root, dirs, files in os.walk("bot"):
            for name in files:
                if str(root).endswith("__pycache__"):
                    continue
                self.load_extension(os.path.join(root, name).replace("\\", ".").replace("/", ".")[:-3])

        self.run(self.token)


if __name__ == "__main__":
    MeowBot()
