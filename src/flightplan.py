import os

import nextcord  # type: ignore
from nextcord.ext import commands  # type: ignore
import logging
import sys

from config import GUILD_ID, DISCORD_TOKEN





class HexBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)






watch_handler = logging.StreamHandler(sys.stdout)
watch_handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))





def main():
    intents = nextcord.Intents.default()
    intents.members = True
    intents.message_content = True

    activity = nextcord.CustomActivity(
        '"Cleared to taxi to Runway L23"')
    
    bot = HexBot(intents=intents, activity=activity)

    for folder in os.listdir("src/cogs"):
        if os.path.exists(os.path.join("src/cogs", folder, "cog.py")):
            print(f"💦💦 cogs.{folder}")
            bot.load_extension(f"cogs.{folder}.cog")
    
   
    async def on_ready():
        print('Kill mE PlEEAAAASe')
        print(f'We have logged in as {bot.user}')

   


    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)

    

    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
