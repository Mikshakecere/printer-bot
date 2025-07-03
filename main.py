import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
from racefetcher import fetch_race_tiles, fetch_relevant_relics
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        try:
            guild = discord.Object(id=GUILD_ID)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')


handler = logging.FileHandler(filename='discord.log',encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(command_prefix="!", intents=intents)

guild = discord.Object(id=GUILD_ID)

@client.tree.command(name="fetch_races", description="Fetch all races for the given ct", guild=guild)
@app_commands.choices(race_type=[
    app_commands.Choice(name="Regular", value="Regular"),
    app_commands.Choice(name="Banner", value="Banner"),
    app_commands.Choice(name="Relic", value="Relic")
])
async def fetch_races(interaction: discord.Interaction, race_type: app_commands.Choice[str]=None):
    regulars, banners, relics = fetch_race_tiles()
    if race_type == None:
        await interaction.response.send_message("**Regulars (" + str(len(regulars)) + "):**\n" + f"``{regulars}``\n" +
                                                "**Banners (" + str(len(banners)) + "):**\n" + f"``{banners}``\n" +
                                                "**Relics (" + str(len(relics)) + "):**\n" + f"``{relics}``")
    if race_type.value == "Regular":
        await interaction.response.send_message("**Regulars (" + str(len(regulars)) + "):**\n" + f"``{regulars}``")
    elif race_type.value == "Banner":
        await interaction.response.send_message("**Banners (" + str(len(banners)) + "):**\n" + f"``{banners}``")
    elif race_type.value == "Relic":
        await interaction.response.send_message("**Relics (" + str(len(relics)) + "):**\n" + f"``{relics}``")

@client.tree.command(name="fetch_relics", description="Fetch all race relevant relics for the given ct", guild=guild)
async def fetch_relics(interaction: discord.Interaction):
    relics = fetch_relevant_relics()
    await interaction.response.send_message(f"**Race relevant relics (" + str(len(relics)) + "):**\n" + f"``{relics}``")

@client.tree.command(name="fetch_all_info", description="Fetch all info for the given ct", guild=guild)
async def fetch_relics(interaction: discord.Interaction, ct_number: int):
    await interaction.response.send_message(f"Placeholder text for info from ct {ct_number}")

client.run(token)

