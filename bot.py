import discord
from discord.ext import tasks
import buses
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    update.start()
    await tree.sync()

@tasks.loop(seconds=60)
async def update():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=buses.getNumberOfScanias()))

@tree.command(name = "elektryczne", description = "Wypisuje listę autobusów elektrycznych")
async def elektryczne(interaction):
    await interaction.response.send_message(buses.getElectricBuses())

@tree.command(name = "hybrydowe", description = "Wypisuje listę autobusów hybrydowych")
async def elektryczne(interaction):
    await interaction.response.send_message(buses.getHybridBuses())

@tree.command(name = "scania", description = "Wypisuje listę autobusów kradzionych z Oslo")
async def scania(interaction):
    await interaction.response.send_message(buses.getScaniaBuses())

@tree.command(name = "specjalne", description = "Wypisuje listę autobusów nietypowych")
async def scania(interaction):
    await interaction.response.send_message(buses.getSpecialBuses())

client.run(buses.apikey["bot_secret"])

