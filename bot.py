import discord
import re
from discord.ext import tasks
from datetime import datetime
import store
from config import TOKEN, RESET_HOUR, RESET_MINUTE, BAD_WORDS, FINE_PER_SWEAR
from leaderboard import post_leaderboard

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)

def normalize(text):
    return re.sub(r'([aeiouAEIOU])\1+', r'\1', text.lower())

def count_swears(text):
    normalized = normalize(text)
    counts = {}
    for word in sorted(BAD_WORDS, key=len, reverse=True):
        count = normalized.count(word)
        if count > 0:
            counts[word] = count
    return counts

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

    if message.content == "!profile":
        data = store.load()
        entry = data.get(uid)
        embed = discord.Embed(title=f"{username}'s Profile", color=discord.Color.blurple())
        embed.set_thumbnail(url=avatar)
        if entry:
            top_word = max(entry["daily_words"], key=entry["daily_words"].get) if entry["daily_words"] else "Wala"
            embed.add_field(name="Total Swears", value=str(entry["total_count"]), inline=True)
            embed.add_field(name="Total Owed", value=f"PHP {entry['total_count'] * FINE_PER_SWEAR}", inline=True)
            embed.add_field(name="Clean Streak", value=f"{entry['clean_streak']} days", inline=True)
            embed.add_field(name="Most Used Word", value=f"`{top_word}`", inline=True)
        else:
            embed.description = "Wala pang record. Malinis ka pa!"
        await message.channel.send(embed=embed)
        return

    swear_counts = count_swears(message.content)
    if not swear_counts:
        return

    data = store.load()
    prev_streak = data.get(uid, {}).get("clean_streak", 0)

    for word, count in swear_counts.items():
        for _ in range(count):
            store.record_swear(uid, username, avatar, word)

    if prev_streak >= 10:
        top = max(swear_counts, key=swear_counts.get)
        await message.channel.send(f"STREAK SHATTERED! {message.author.mention} just broke a **{prev_streak}-day clean streak** with `{top}`.")

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
