import discord
import requests
import re
import json
import os
import html
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
UPDATE_CHANNEL_ID = int(os.getenv("UPDATE_CHANNEL_ID", "0"))
UPLOAD_CHANNEL_ID = int(os.getenv("UPLOAD_CHANNEL_ID", "0"))
UPDATE_WEBHOOK_URL = os.getenv("UPDATE_WEBHOOK_URL")
UPLOAD_WEBHOOK_URL = os.getenv("UPLOAD_WEBHOOK_URL")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
PROCESSED_FILE = os.getenv("PROCESSED_FILE", "last_processed.json")

bot = commands.Bot(command_prefix="!", self_bot=True)

if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, "r") as f:
        processed_ids = json.load(f)
else:
    processed_ids = {}

def save_processed(channel_id, message_id):
    processed_ids[str(channel_id)] = message_id
    with open(PROCESSED_FILE, "w") as f:
        json.dump(processed_ids, f)

def get_steam_details(appid):
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
        response = requests.get(url)
        data = response.json()
        app_data = data[str(appid)]['data']

        return {
            "name": app_data.get("name", f"App {appid}"),
            "short_description": html.unescape(app_data.get("short_description", "No description available.")),
            "header_image": app_data.get("header_image"),
            "logo": app_data.get("header_image").replace("header.jpg", "logo_2x.png"),
            "steamdb_url": f"https://steamdb.info/app/{appid}/"
        }
    except Exception as e:
        print(f"Steam API Error for AppID {appid}: {e}")
        return None

def parse_depots(field_value):
    return re.findall(r"(\d+): \d+ -> (\d+)", field_value)

async def process_message(message):
    if message.author.id != 1326675340684296242 or not message.embeds:
        return

    embed = message.embeds[0]
    description = html.unescape(embed.description or "")

    match = re.search(r'\*\*AppID:\*\* (\d+)', description)
    appid = match.group(1) if match else None
    steam_data = get_steam_details(appid) if appid else None

    webhook_url = UPLOAD_WEBHOOK_URL if message.channel.id == UPLOAD_CHANNEL_ID else UPDATE_WEBHOOK_URL
    username = "Ryuu: uploads" if message.channel.id == UPLOAD_CHANNEL_ID else "Ryuu: updates"
    avatar_url = "https://cdn.discordapp.com/avatars/1368694530924085328/1d1146d028ff076152277295be55f116.webp"

    payload = {
        "username": username,
        "avatar_url": avatar_url,
        "embeds": []
    }

    if message.channel.id == UPDATE_CHANNEL_ID and steam_data and embed.fields:
        depot_changes = parse_depots(embed.fields[0].value)
        for depot_id, manifest in depot_changes:
            new_embed = {
                "type": "rich",
                "title": f"{steam_data['name']} ({appid})",
                "description": f"- Updated depot `{depot_id}` to manifest `{depot_id}_{manifest}`",
                "color": 0x2f3136,
                "thumbnail": {"url": steam_data['logo']} if steam_data else None,
                "image": {"url": steam_data['header_image']}
            }
            payload["embeds"].append(new_embed)
    else:
        new_embed = {
            "type": "rich",
            "title": f"{steam_data['name']} ({appid})" if steam_data else embed.title,
            "description": steam_data['short_description'] if steam_data else description,
            "url": steam_data['steamdb_url'] if steam_data else None,
            "color": 2894892,
            "thumbnail": {"url": steam_data['logo']} if steam_data else None,
            "image": {"url": steam_data['header_image']} if steam_data else (embed.image.url if embed.image else None)
        }
        payload["embeds"].append(new_embed)

    if webhook_url:
        requests.post(webhook_url, json=payload)
    save_processed(message.channel.id, message.id)

@bot.event
async def on_ready():
    print("🤖 Bot is running!")
    for channel_id in (UPDATE_CHANNEL_ID, UPLOAD_CHANNEL_ID):
        channel = bot.get_channel(channel_id)
        if not channel:
            continue
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=1):
                last_id = processed_ids.get(str(channel_id))
                if str(message.id) != str(last_id):
                    await process_message(message)

@bot.event
async def on_message(message):
    if message.channel.id not in (UPDATE_CHANNEL_ID, UPLOAD_CHANNEL_ID):
        return
    last_id = processed_ids.get(str(message.channel.id))
    if str(message.id) == str(last_id):
        return
    await process_message(message)

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set.")
bot.run(TOKEN)