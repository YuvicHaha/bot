import os
import threading
import discord
from discord import app_commands
import requests
from flask import Flask

# 🔒 Environment Variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BRIDGE_URL = os.getenv("BRIDGE_URL")
PORT = int(os.getenv("PORT", 3000))

# 🌐 Flask server for Render/UptimeRobot
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Discord Bot is alive!"

@app.route("/ping")
def ping():
    return "pong", 200

def run_web():
    app.run(host="0.0.0.0", port=PORT)

# 🚀 Start Flask server in a thread
threading.Thread(target=run_web).start()

# 🤖 Discord Bot Setup
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Logged in as {self.user}")

client = MyClient()

# 🔧 /freeze <key>
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

# 🔧 /unfreeze <key>
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

# 🔧 /kill [key]
@client.tree.command(name="kill", description="Kill a specific client or all if no key is provided")
@app_commands.describe(key="Optional client key to target (leave blank for all)")
async def kill(interaction: discord.Interaction, key: str = None):
    try:
        target = key or "all"
        res = requests.post(f"{BRIDGE_URL}/command", json={"key": target, "action": "kill"})
        if res.status_code == 200:
            msg = f"☠️ Kill sent to `{target}`" if key else "☠️ Kill sent to all clients."
            await interaction.response.send_message(msg)
        else:
            await interaction.response.send_message(f"❌ Failed to send kill to `{target}`")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}")

# 🔧 /kick <message> [key]
@client.tree.command(name="kick", description="Kick a client (or all) with a message")
@app_commands.describe(
    message="Kick message",
    key="Optional client key to target (leave blank for all)"
)
async def kick(interaction: discord.Interaction, message: str, key: str = None):
    try:
        target = key or "all"
        res = requests.post(f"{BRIDGE_URL}/command", json={"key": target, "action": "kick", "message": message})
        if res.status_code == 200:
            msg = f"👢 Kick sent to `{target}`: {message}" if key else f"👢 Kick sent to all: {message}"
            await interaction.response.send_message(msg)
        else:
            await interaction.response.send_message(f"❌ Failed to send kick to `{target}`")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}")

# 🟢 Run the bot
client.run(DISCORD_TOKEN)
