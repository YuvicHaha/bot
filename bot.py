import os
import discord
from discord import app_commands
import requests
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BRIDGE_URL = os.getenv("BRIDGE_URL")
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Logged in as {self.user}")

client = MyClient()
@client.tree.command(name="freeze", description="Freeze a Roblox client by key")
@app_commands.describe(key="The Roblox client's generated key")
async def freeze(interaction: discord.Interaction, key: str):
    try:
        res = requests.post(f"{BRIDGE_URL}/command", json={"key": key, "action": "freeze"})
        if res.status_code == 200:
            await interaction.response.send_message(f"✅ Freeze sent to `{key}`")
        else:
            await interaction.response.send_message(f"❌ Key `{key}` not found.")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}")
@client.tree.command(name="unfreeze", description="Unfreeze a Roblox client by key")
@app_commands.describe(key="The Roblox client's generated key")
async def unfreeze(interaction: discord.Interaction, key: str):
    try:
        res = requests.post(f"{BRIDGE_URL}/command", json={"key": key, "action": "unfreeze"})
        if res.status_code == 200:
            await interaction.response.send_message(f"🧊 Unfreeze sent to `{key}`")
        else:
            await interaction.response.send_message(f"❌ Key `{key}` not found.")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}")

# ✅ Start the bot
client.run(DISCORD_TOKEN)
