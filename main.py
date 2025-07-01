import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
from racefetcher import fetch_ct_tiles
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
async def fetch_races(interaction: discord.Interaction):
    regulars, banners, relics = fetch_ct_tiles()
    await interaction.response.send_message(f"Regulars (" + str(len(regulars)) + "):\n" + f"{regulars}\n" +
                                            f"Banners (" + str(len(banners)) + "):\n" + f"{banners}\n" +
                                            f"Relics (" + str(len(relics)) + "):\n" + f"{relics}")

@client.tree.command(name="fetch_relics", description="Fetch all race relevant relics for the given ct", guild=guild)
async def fetch_relics(interaction: discord.Interaction, ct_number: int):
    await interaction.response.send_message(f"Placeholder text for race relevant relics from ct {ct_number}")

@client.tree.command(name="fetch_all_info", description="Fetch all info for the given ct", guild=guild)
async def fetch_relics(interaction: discord.Interaction, ct_number: int):
    await interaction.response.send_message(f"Placeholder text for info from ct {ct_number}")

client.run(token)

