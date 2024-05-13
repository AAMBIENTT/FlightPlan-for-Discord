import random

import nextcord  # type: ignore
from nextcord.ext import commands  # type: ignore

from config import *


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("❓ " + self.__class__.__qualname__ + " STARTED")
    
    @nextcord.slash_command(description="Display help information for all commands.", guild_ids=[GUILD_ID])
    async def help(self, interaction: nextcord.Interaction):
        # Generate a random color for the embed
        embed = nextcord.Embed(title="Bot Commands",
                      description="Here are the available commands and their usage examples:",
                      colour=0xff80ff)

        embed.set_author(name="",
                        url="")

        embed.add_field(name="/flightplan",
                        value="Using SimBrief URLs, fetch flight info & aircraft images..\n**Example:** `/flightplan [simbrief url]`",
                        inline=False)
        embed.add_field(name="/modifyflight",
                        value="Using SimBrief URLs, modify an existing flightplan and recieve and updated, shortened URL.\n**Example:** `/modify_flight url: [URL] flight_number: 443 airline: DAL aircraft: A339`",
                        inline=False)


        embed.set_footer(text="❤️ Made with love by Mono x Mellow")

        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
    