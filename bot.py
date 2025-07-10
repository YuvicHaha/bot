import os
import threading
import discord
from discord import app_commands
import requests
from flask import Flask
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BRIDGE_URL = os.getenv("BRIDGE_URL")
PORT = int(os.getenv("PORT", 3000))  # Default to 3000
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Discord Bot is alive!"

@app.route("/ping")
def ping():
    return "pong", 200

def run_web():
    app.run(host="0.0.0.0", port=PORT)
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
threading.Thread(target=run_web).start()
client.run(DISCORD_TOKEN)
