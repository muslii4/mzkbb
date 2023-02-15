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
    if datetime.datetime.now().strftime("%u.%H:%M") in buses.apikey["notification_times"]:
        message_channel = await client.fetch_user(buses.apikey["owner_id"])
        msg = buses.getRemainingBuses()
        if msg != "brak":
            await message_channel.send(msg)

@tree.command(name = "nowe", description = "Wypisuje listę niewpisanych autobusów",
              guilds=[discord.Object(id=buses.apikey["owner_guild"]), discord.Object(id=buses.apikey["owner_id"])])
async def nowe(interaction):
    await interaction.response.send_message(buses.getRemainingBuses())

@tree.command(name = "elektryczne", description = "Wypisuje listę autobusów elektrycznych")
async def elektryczne(interaction):
    await interaction.response.send_message(buses.getElectricBuses())

@tree.command(name = "scania", description = "Wypisuje listę autobusów kradzionych z Oslo")
async def scania(interaction):
    await interaction.response.send_message(buses.getScaniaBuses())

client.run(buses.apikey["bot_secret"])