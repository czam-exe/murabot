import discord
from store import load, reset
from config import FINE_PER_SWEAR

async def post_leaderboard(bot, channel):
    data = load()
    if not data:
        await channel.send("📭 No data recorded today.")
        reset()
        return

    swearers = {uid: v for uid, v in data.items() if v["daily_count"] > 0}
    saints = [v for v in data.values() if v["sent_message_today"] and v["daily_count"] == 0]
    total_today = sum(v["daily_count"] for v in data.values())

    champion_embed = None
    if swearers:
        champ_id = max(swearers, key=lambda uid: swearers[uid]["daily_count"])
        champ = swearers[champ_id]
        top_word = max(champ["daily_words"], key=champ["daily_words"].get)
        fine = champ["daily_count"] * FINE_PER_SWEAR
        champion_embed = discord.Embed(title="🏆 Swear Champion of the Day", color=discord.Color.red())
        champion_embed.set_thumbnail(url=champ["avatar_url"])
        champion_embed.add_field(name="User", value=champ["username"], inline=True)
        champion_embed.add_field(name="Swears", value=str(champ["daily_count"]), inline=True)
        champion_embed.add_field(name="Most Used", value=f"`{top_word}`", inline=True)
        champion_embed.add_field(name="💸 Owes Jar", value=f"PHP {fine}", inline=True)

    saint_names = ", ".join(s["username"] for s in saints) or "None"
    saint_embed = discord.Embed(title="😇 Saints of the Day", description=saint_names, color=discord.Color.green())

    yesterday = getattr(post_leaderboard, "_yesterday_total", None)
    if yesterday is None:
        trend = "📊 First day on record!"
    elif total_today > yesterday:
        trend = f"📈 Dirtier than yesterday ({yesterday} → {total_today})"
    elif total_today < yesterday:
        trend = f"📉 Cleaner than yesterday ({yesterday} → {total_today})"
    else:
        trend = f"➡️ Same as yesterday ({total_today})"
    post_leaderboard._yesterday_total = total_today

    index_embed = discord.Embed(title="🌡️ Server Foulness Index", description=trend, color=discord.Color.orange())

    if swearers:
        jar_lines = []
        for uid, v in sorted(swearers.items(), key=lambda x: -x[1]["daily_count"]):
            top = max(v["daily_words"], key=v["daily_words"].get)
            jar_lines.append(f"**{v['username']}** — {v['daily_count']} swears | Most used: `{top}` | Owes: PHP {v['daily_count'] * FINE_PER_SWEAR}")
        jar_embed = discord.Embed(title="💰 Profanity Jar", description="\n".join(jar_lines), color=discord.Color.gold())
    else:
        jar_embed = discord.Embed(title="💰 Profanity Jar", description="Empty today! Everyone was clean. 🎉", color=discord.Color.gold())

    await channel.send("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    await channel.send(embed=saint_embed)
    await channel.send(embed=index_embed)
    await channel.send(embed=jar_embed)
    if champion_embed:
        await channel.send(embed=champion_embed)
    await channel.send("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    reset()
