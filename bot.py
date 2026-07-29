import discord
from discord.ext import tasks
from datetime import datetime
import store
from config import TOKEN, RESET_HOUR, RESET_MINUTE, BAD_WORDS
from leaderboard import post_leaderboard

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)

def detect_swear(text):
    low = text.lower()
    for word in sorted(BAD_WORDS, key=len, reverse=True):
        if word in low:
            return word
    return None

def get_channel(guild):
    for ch in guild.text_channels:
        if ch.permissions_for(guild.me).send_messages:
            return ch
    return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    daily_reset.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    uid = str(message.author.id)
    username = str(message.author)
    avatar = str(message.author.display_avatar.url)
    store.mark_active(uid, username, avatar)

    if message.content == "!leaderboard":
        ch = get_channel(message.guild)
        if ch:
            await post_leaderboard(bot, ch)
        return

    matched = detect_swear(message.content)
    if not matched:
        return
    data = store.load()
    prev_streak = data.get(uid, {}).get("clean_streak", 0)
    store.record_swear(uid, username, avatar, matched)
    if prev_streak >= 10:
        await message.channel.send(f" **STREAK SHATTERED!** {message.author.mention} just broke a **{prev_streak}-day clean streak** with `{matched}`. ")
    data = store.load()
    data[uid]["clean_streak"] = 0
    store.save(data)

@tasks.loop(minutes=1)
async def daily_reset():
    now = datetime.now()
    if now.hour == RESET_HOUR and now.minute == RESET_MINUTE:
        data = store.load()
        for uid, v in data.items():
            if v["daily_count"] == 0 and v["sent_message_today"]:
                v["clean_streak"] += 1
            elif v["daily_count"] > 0:
                v["clean_streak"] = 0
        store.save(data)
        for guild in bot.guilds:
            ch = get_channel(guild)
            if ch:
                await post_leaderboard(bot, ch)

bot.run(TOKEN)
