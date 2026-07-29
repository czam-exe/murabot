import discord
import random
from datetime import datetime
from store import load, reset
from config import FINE_PER_SWEAR

BIBLE_VERSES = [
    ('"Ang mabuting tao ay nagsasalita ng mabuti."', 'Mateo 12:35'),
    ('"Ang dila ay maliit na bahagi ng katawan, ngunit napakalaki ng magagawa nito."', 'Santiago 3:5'),
    ('"Huwag lumabas sa inyong bibig ang anumang masamang salita."', 'Efeso 4:29'),
    ('"Ang maingat sa salita ay maingat din sa buong buhay."', 'Santiago 3:2'),
    ('"Ang puso ng matuwid ay nag-iisip bago magsalita."', 'Kawikaan 15:28'),
    ('"Ang malambot na sagot ay nagpapatahimik ng galit."', 'Kawikaan 15:1'),
    ('"Ang bawat salita mo ay dapat magbigay ng buhay, hindi kamatayan."', 'Kawikaan 18:21'),
    ('"Magingat sa inyong mga salita, sapagkat kayo ay susukatin sa mga ito."', 'Mateo 12:36'),
]

async def post_leaderboard(bot, channel):
    data = load()
    if not data:
        await channel.send("Walang data ngayon.")
        reset()
        return

    swearers = {uid: v for uid, v in data.items() if v["daily_count"] > 0}
    saints = [v for v in data.values() if v["sent_message_today"] and v["daily_count"] == 0]
    total_today = sum(v["daily_count"] for v in data.values())
    today_str = datetime.now().strftime("%B %d, %Y")

    verse, reference = random.choice(BIBLE_VERSES)
    verse_embed = discord.Embed(description=f"*{verse}*\n— **{reference}**", color=discord.Color.blurple())

    embed = discord.Embed(title="Mura Daily Leaderboard", description=today_str, color=discord.Color.dark_red())

    if swearers:
        champ_id = max(swearers, key=lambda uid: swearers[uid]["daily_count"])
        champ = swearers[champ_id]
        top_word = max(champ["daily_words"], key=champ["daily_words"].get)
        embed.set_thumbnail(url=champ["avatar_url"])
        embed.add_field(
            name="Pinaka Gago Ngayong Araw",
            value=f"**{champ['username']}**\n{champ['daily_count']} swears | Most used: `{top_word}` | Owes: PHP {champ['daily_count'] * FINE_PER_SWEAR}",
            inline=True
        )
    else:
        embed.add_field(name="Pinaka Gago Ngayong Araw", value="Walang gago ngayon.", inline=True)

    saint_names = "\n".join(f"• {s['username']}" for s in saints) or "Wala"
    embed.add_field(name="Saints of the Day", value=saint_names, inline=True)

    embed.add_field(name="\u200b", value="\u200b", inline=False)

    if swearers:
        jar_lines = []
        for i, (uid, v) in enumerate(sorted(swearers.items(), key=lambda x: -x[1]["daily_count"]), 1):
            top = max(v["daily_words"], key=v["daily_words"].get)
            jar_lines.append(f"`{i}.` **{v['username']}** — {v['daily_count']} swears | `{top}` | PHP {v['daily_count'] * FINE_PER_SWEAR}")
        embed.add_field(name="Profanity Jar", value="\n".join(jar_lines), inline=False)
    else:
        embed.add_field(name="Profanity Jar", value="Nabuhusan ng holy water ang lahat.", inline=False)

    yesterday = getattr(post_leaderboard, "_yesterday_total", None)
    if yesterday is None:
        trend = "Unang araw ng record."
    elif total_today > yesterday:
        trend = f"Mas masahol ngayon ({yesterday} -> {total_today})"
    elif total_today < yesterday:
        trend = f"Mas masahol kahapon ({yesterday} -> {total_today})"
    else:
        trend = f"Tamang timpla ({total_today})"
    post_leaderboard._yesterday_total = total_today

    embed.add_field(name="Server Foulness Index", value=trend, inline=False)
    embed.set_footer(text="Mura Bot | Daily Reset")

    await channel.send(embed=verse_embed)
    await channel.send(embed=embed)
    reset()
